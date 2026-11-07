#!/usr/bin/env bash
# ZANS Racing: make a read-only Google robot for Search Console.
# Run it once in Google Cloud Shell, signed in to Google as the Search Console owner.
# It makes a free Google Cloud project with one robot account. The robot has NO key and
# NO password. Only GitHub jobs in github.com/zankendo2-ship-it can use it. Nothing is paid for.
# Safe to run again: it re-uses what it already made.
set -uo pipefail

GH_OWNER_ID=332616699                 # github.com/zankendo2-ship-it (number never changes)
PROJECT=zans-racing-332616699         # Google Cloud project for ZANS robots
ROBOT=zans-search                     # robot name
EMAIL="$ROBOT@$PROJECT.iam.gserviceaccount.com"
POOL=zans-github
PROVIDER=github-actions

say()  { printf '\n\033[1;32m%s\033[0m\n' "$*"; }
stop() { printf '\n\033[1;31mSTOPPED: %s\033[0m\nTake a screenshot of this screen and send it to Claude.\n' "$*"; exit 1; }
# try a command up to 8 times, 10 seconds apart (new Google projects take a moment to be ready)
retry() { local n; for n in 1 2 3 4 5 6 7 8; do "$@" >/dev/null 2>/tmp/zans_err && return 0; sleep 10; done; cat /tmp/zans_err >&2; return 1; }

say "1/5 Making the ZANS project..."
if ! gcloud projects describe "$PROJECT" >/dev/null 2>&1; then
  gcloud projects create "$PROJECT" --name="ZANS Racing robots" --quiet || stop "Google would not make the project"
fi
NUMBER=""
for n in 1 2 3 4 5 6; do
  NUMBER=$(gcloud projects describe "$PROJECT" --format="value(projectNumber)" 2>/dev/null) && [ -n "$NUMBER" ] && break
  sleep 5
done
[ -n "$NUMBER" ] || stop "could not read the new project"

say "2/5 Switching on Search Console for it (about a minute)..."
retry gcloud services enable searchconsole.googleapis.com iam.googleapis.com \
  iamcredentials.googleapis.com sts.googleapis.com --project="$PROJECT" --quiet \
  || stop "Google would not switch the services on"

say "3/5 Making the robot (no key, no password)..."
if ! gcloud iam service-accounts describe "$EMAIL" --project="$PROJECT" >/dev/null 2>&1; then
  retry gcloud iam service-accounts create "$ROBOT" --project="$PROJECT" \
    --display-name="ZANS Search Console robot (read only)" --quiet || stop "Google would not make the robot"
fi

say "4/5 Letting only zankendo2-ship-it GitHub jobs use it..."
if ! gcloud iam workload-identity-pools describe "$POOL" --project="$PROJECT" --location=global >/dev/null 2>&1; then
  retry gcloud iam workload-identity-pools create "$POOL" --project="$PROJECT" --location=global \
    --display-name="ZANS GitHub" --quiet || stop "Google would not make the GitHub link"
fi
if ! gcloud iam workload-identity-pools providers describe "$PROVIDER" --project="$PROJECT" \
     --location=global --workload-identity-pool="$POOL" >/dev/null 2>&1; then
  retry gcloud iam workload-identity-pools providers create-oidc "$PROVIDER" --project="$PROJECT" \
    --location=global --workload-identity-pool="$POOL" --display-name="GitHub Actions" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.repository_owner_id=assertion.repository_owner_id" \
    --attribute-condition="assertion.repository_owner_id=='$GH_OWNER_ID'" --quiet \
    || stop "Google would not make the GitHub link"
fi

say "5/5 Handing the robot to those GitHub jobs..."
MEMBER="principalSet://iam.googleapis.com/projects/$NUMBER/locations/global/workloadIdentityPools/$POOL/attribute.repository_owner_id/$GH_OWNER_ID"
for ROLE in roles/iam.workloadIdentityUser roles/iam.serviceAccountTokenCreator; do
  retry gcloud iam service-accounts add-iam-policy-binding "$EMAIL" --project="$PROJECT" \
    --role="$ROLE" --member="$MEMBER" --quiet || stop "Google would not hand the robot over"
done

G=$(printf '%s' "$NUMBER" | sed 's/.\{4\}/& /g')
printf '\n\033[1;32m==============================\n DONE - the robot is ready\n==============================\033[0m\n'
printf '\n Robot email:\n %s\n' "$EMAIL"
printf '\n Project number:\n \033[1m%s\033[0m\n' "$G"
printf '\n Now take a screenshot of this\n screen and send it to Claude.\n\n'
