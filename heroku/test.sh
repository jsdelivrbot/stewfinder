curl -X POST http://stewfinder-backend.us-west-2.elasticbeanstalk.com/api/soops/ \
    -H 'Content-Type: application/json' \
    -d @- <<EOF
{
    "title": "a",
    "details": "b",
    "day": "c",
    "outUrl": "d",
    "food": "e",
    "when": "f",
    "location": "g"
}
EOF
