npm run build
aws s3 rm s3://stewfinder-frontend/ --recursive
aws s3 cp build/ s3://stewfinder-frontend/ --recursive
