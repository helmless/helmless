#!/usr/bin/env bash

set -e
export PATH=$PATH:/usr/local/bin

if which helm &> /dev/null $? != 0 ; then
    echo "HELM must be installed"
    exit 1
fi

for chart in $(find . -name 'Chart.yaml'); do
    chart_dir=$(dirname "$chart")
    echo "Running linting in $chart_dir"
    (cd "$chart_dir" && helm dependency build && helm lint . --set-string project=my-project --set-string name=my-service)
done
