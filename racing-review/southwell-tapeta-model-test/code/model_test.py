"""Southwell AW method v2.3 v v2.4 on Tapeta races, model based, H1 (7 Dec 2021-31 May 2024) v H2 (1 Jun 2024-).
Run from a checkout of the racing branch with history fetched (scripts/fetch_history.sh):
  python3 model_test.py --mode strict_surface|asis|strict_only|surface_only --out result.json
asis          = the live walk's behaviour: races ordered by date only, same-day results visible to later races, mixed surfaces.
strict_only   = every feature uses results from earlier DATES only (a day's races are all scored before any is added).
surface_only  = races on a course's pre-switch AW surface (courses.json surface_since) are dropped everywhere (state, jockey/horse history, samples).
strict_surface= both.
Weights are fitted on races before 2021-12-07 only (no test race in training). Speed standards use fit_before 2026-01-01 (as the live rebuild): paired v2.3/v2.4 comparison unaffected."""
import argparse, glob, json, math, os, random, sys
from collections import defaultdict
from datetime import date as Date
sys.path.insert(0, os.getcwd())
import numpy as np
from predict import features as F, model as M
from methods import audit as AU

ap = argparse.ArgumentParser(); ap.add_argument('--mode', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args()
STRICT = a.mode in ('strict_only', 'strict_surface'); SURF = a.mode in ('surface_only', 'strict_surface')
SINCE, H2 = '2021-12-07', '2024-06-01'
cs = json.load(open('config/courses.json')); cs = cs.get('courses', cs)
SS = {k: (v.get('surface_since') or {}).get('AW_FLAT') for k, v in cs.items() if (v.get('surface_since') or {}).get('AW_FLAT')}
drop = lambda r: SURF and r['disc'] == 'AW_FLAT' and SS.get(r['course_id']) and r['date'] < SS[r['course_id']]
paths = sorted(glob.glob('history/*.csv.gz'))

# ---------- walk (model features) ----------
figs, _ = F.speed_figures(paths, '2026-01-01')
races = F.load_rows(paths)
excluded = defaultdict(int)
if SURF:
    kept = []
    for r in races:
        if drop(r): excluded['pre-switch AW race dropped everywhere'] += 1
        else: kept.append(r)
    races = kept
if STRICT: races = sorted(races, key=lambda r: r['date'])
state = F.State(); samples = []
def do_race(race):
    day = F.ordinal(race['date']); fam = F.fam_of(race['disc']); rn = race['runners']
    if race['date'] >= '2019-01-01' and len(rn) >= 4:
        sps = [r['sp'] for r in rn]; w = [i for i, r in enumerate(rn) if r['pos'] == 1]
        if all(sps) and len(w) == 1:
            raws = [state.runner(r['horse'], day, fam, race['course_id'], race['furlongs'], r['trainer'], r['jockey'], going=race['going'], race_class=race['cls']) for r in rn]
            code = 'JUMPS' if fam == 'JUMPS' else race['disc']
            rows, _ = F.race_vectors(raws, [r['lbs'] for r in rn], [r['or'] for r in rn], race['disc'], (race['course_id'], code, race['furlongs'], race['going']), [r['draw'] for r in rn], race['handicap'], hg=[r.get('hg') for r in rn])
            book = sum(1 / s for s in sps); samples.append((race, rows, w[0], [1 / s / book for s in sps], sps))
def add_race(race):
    day = F.ordinal(race['date']); fam = F.fam_of(race['disc'])
    inc = F.stewards_incidents()
    for r in race['runners']:
        state.add(r['horse'], day, fam, race['course_id'], race['furlongs'], race['going'], r['pos'], r['rpr'], figs.get((race['key'], r['horse'])), r['lbs'], r['style'], r['trainer'], r['jockey'], race['cls'], hg=r.get('hg'), sex=r.get('sex'),
                  jm='JUMPING' in inc.get((race['date'], r['horse']), ()), fell=r.get('pos_code') in F.FALLERS)
if STRICT:
    by_day = defaultdict(list)
    for r in races: by_day[r['date']].append(r)
    for d in sorted(by_day):
        for r in by_day[d]: do_race(r)
        for r in by_day[d]: add_race(r)
else:
    for r in races: do_race(r); add_race(r)
print('walk done', len(samples), flush=True)

# ---------- model fit before SINCE (FLAT family incl AW), joint (with log market) ----------
S = [s for s in samples if F.fam_of(s[0]['disc']) == 'FLAT' and len(s[1]) >= 2]
def pack(ss, market):
    X, st, won = M._pack(ss); mk = np.concatenate([s[3] for s in ss])
    return (np.column_stack([X, np.log(np.clip(mk, 1e-4, 1))]) if market else X), st, won
tr = [s for s in S if '2019-01-01' <= s[0]['date'] < SINCE]
W = {True: M.fit(*pack(tr, True)), False: M.fit(*pack(tr, False))}
test = [s for s in S if s[0]['course_id'] == 'southwell' and s[0]['disc'] == 'AW_FLAT' and s[0]['date'] >= SINCE]
print('train', len(tr), 'test', len(test), flush=True)

# ---------- rule flags (methods.audit definitions) on the same races ----------
arace = AU.load(paths, AU.race_info('data/results_uki.csv.gz'))
if SURF: arace = [r for r in arace if not (r['disc'] == 'AW_FLAT' and SS.get(r['course_id']) and r['date'] < SS[r['course_id']])]
hist = defaultdict(list); jr, jruns = set(), defaultdict(list)
flagmap = {}
def aflags(r):
    r['fam'] = 'JUMPS' if r['disc'] in ('HURDLE', 'CHASE', 'NHF') else 'FLAT'
    sps = [x['sp'] for x in r['runners']]; w = [x for x in r['runners'] if x['pos'] == 1]
    if r['course_id'] == 'southwell' and r['disc'] == 'AW_FLAT' and r['date'] >= SINCE and all(sps) and len(r['runners']) >= 4 and len(w) == 1:
        flagmap[(r['date'], r['course_id'], tuple(x['horse'] for x in r['runners']))] = AU.flags_for_race(r, hist, jr, jruns)
def aadd(r):
    day = Date.fromisoformat(r['date']).toordinal()
    for x in r['runners']:
        hist[x['horse']].append({'day': day, 'fam': r['fam'], 'course_id': r['course_id'], 'furlongs': r['furlongs'], 'going': r['going'], 'pos': x['pos'], 'won': x['pos'] == 1, 'rpr': x['rpr'], 'handicap': r['handicap'], 'comment': x['comment']})
        if x['jockey']: jr.add((x['horse'], x['jockey'])); jruns[x['jockey']].append((day, x['pos'] == 1))
if STRICT:
    by_day = defaultdict(list)
    for r in arace: by_day[r['date']].append(r)
    for d in sorted(by_day):
        for r in by_day[d]: aflags(r)
        for r in by_day[d]: aadd(r)
else:
    for r in sorted(arace, key=lambda r: r['date']): aflags(r); aadd(r)

RULES = {'exact_rpr': 'Top EXACT-conditions RPR (trip +-1f + same going)', 'top_rpr': 'Top recent RPR in race (best of last 3)', 'ground_spec': 'Rule 5.1 ground exclusivity (won on exact going; 1-2 in field have)',
         'lone_leader': 'Lone front-runner (only habitual leader in race)', 'slow_start': 'HR8 slow starter (2+ of last 4) in a 5-6f race', 'leader': 'Usual front-runner (led in half of last 6)', 'older': 'HR5 age 6+'}
V23 = dict(exact_rpr=1.05, top_rpr=1.03, ground_spec=1.10, lone_leader=1.06, slow_start=0.94, leader=0.96, older=0.98)
V24 = dict(exact_rpr=1.00, top_rpr=1.03, ground_spec=1.08, lone_leader=1.00, slow_start=1.00, leader=0.96, older=0.98)
recs, miss = [], 0
for race, rows, wi, mk, sps in test:
    key = (race['date'], race['course_id'], tuple(r['horse'] for r in race['runners']))
    fl = flagmap.get(key)
    if fl is None: miss += 1; continue
    Xa = np.array(rows, float); m = np.clip(np.array(mk, float), 1e-4, 1)
    z = np.column_stack([Xa, np.log(m)]) @ W[True]; pj = np.exp(z - z.max()); pj /= pj.sum()
    zf = Xa @ W[False]; pf = np.exp(zf - zf.max()); pf /= pf.sum()
    def over(p, fac):
        f = np.ones(len(p))
        for i, fd in enumerate(fl):
            for k, nm in RULES.items():
                if fd.get(nm) and not (k == 'slow_start' and not (5 <= race['furlongs'] <= 6.5)): f[i] *= fac[k]
        q = p * f; return q / q.sum()
    rec = dict(date=race['date'], win=wi, n=len(rows), mk=m)
    for nm, p in (('joint', pj), ('form', pf)):
        rec[nm + '_base'] = p; rec[nm + '_v23'] = over(p, V23); rec[nm + '_v24'] = over(p, V24)
    recs.append(rec)
print('scored', len(recs), 'unmatched flag rows', miss, flush=True)

# ---------- metrics with bootstrap intervals ----------
rng = random.Random(7)
def met(rs, nm):
    hit = np.array([int(np.argmax(r[nm]) == r['win']) for r in rs], float); ll = np.array([-math.log(max(r[nm][r['win']], 1e-9)) for r in rs])
    return hit, ll
def ci(x, reps=2000):
    n = len(x); b = sorted(float(np.mean([x[rng.randrange(n)] for _ in range(n)])) for _ in range(reps)); return [round(b[int(.025 * reps)], 4), round(b[int(.975 * reps)], 4)]
out = dict(mode=a.mode, excluded=dict(excluded), train_races=len(tr), test_scored=len(recs), unmatched=miss, halves={})
for hn, sel in (('H1 2021-12-07..2024-05-31', lambda r: r['date'] < H2), ('H2 2024-06-01..', lambda r: r['date'] >= H2), ('ALL', lambda r: True)):
    rs = [r for r in recs if sel(r)]; res = dict(races=len(rs))
    for base in ('joint', 'form'):
        d = {}
        for v in ('base', 'v23', 'v24'):
            h, l = met(rs, f'{base}_{v}'); d[v] = dict(top_hit=round(float(h.mean()), 4), top_hit_ci=ci(h, 1000), logloss=round(float(l.mean()), 4), logloss_ci=ci(l, 1000))
        h3, l3 = met(rs, f'{base}_v23'); h4, l4 = met(rs, f'{base}_v24')
        d['v24_minus_v23'] = dict(top_hit=round(float((h4 - h3).mean()), 4), top_hit_ci=ci(h4 - h3), logloss=round(float((l4 - l3).mean()), 5), logloss_ci=ci(l4 - l3))
        res[base] = d
    mh = np.array([int(np.argmax(r['mk']) == r['win']) for r in rs], float); ml = np.array([-math.log(r['mk'][r['win']]) for r in rs])
    res['market'] = dict(top_hit=round(float(mh.mean()), 4), logloss=round(float(ml.mean()), 4))
    out['halves'][hn] = res
json.dump(out, open(a.out, 'w'), indent=1); print(json.dumps(out, indent=1)[:3000])
