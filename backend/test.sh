curl -X POST http://stewfinder-backend.us-west-2.elasticbeanstalk.com/api/soops/ \
    -d @- <<EOF
    {
        "title": "asdf",
        "details": "asdfasdf",
        "day": "6/22/2018",
        "outUrl": "asdf",
        "food": "free",
        "when": "Every Friday until Jul. 27, 11:15am-noon;...",
        "location": null
    }
EOF
