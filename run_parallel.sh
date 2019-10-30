#! /bin/bash
set -x
PORT=30807

function main {
    JOBS="${1:-10}"
    FRACTION="$(echo "100/$JOBS * .1" | bc)"

    time parallel --progress -j $JOBS curl --silent --insecure --globoff "'http://localhost:${PORT}/current_weather?latitude={1}&longitude=44.44'" -o ./temp/out{1}.json ::: $(seq 30 $FRACTION 40)

}

main "$@"
