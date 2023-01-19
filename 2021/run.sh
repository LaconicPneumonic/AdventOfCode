#!/usr/bin/env bash
# check if image exists
# build image otherwise

CONTAINER_NAME="aoc2021"

if [[ $(docker images "$CONTAINER_NAME" --format "{{.Repository}}" ) ]]; then
    echo "container exists"

else
    echo "building container"
    docker build . -f DOCKERFILE -t $CONTAINER_NAME
fi

# cp stuff in there

CONTAINER_ID=$(docker ps --filter "name=$CONTAINER_NAME" --format "{{.ID}}")

if [  -z "$CONTAINER_ID" ];
then
    echo "RUNNING CONTAINER"
    docker run -dit --name $CONTAINER_NAME $CONTAINER_NAME bash
    CONTAINER_ID=$(docker ps --filter "name=$CONTAINER_NAME" --format "{{.ID}}")
    echo "CONTAINER ID IS $CONTAINER_ID"

fi

docker start $CONTAINER_ID


# execute the command!
docker cp $1/ $CONTAINER_ID:/usr/src/aoc

echo "RUNNING"
echo "-------"
docker exec $CONTAINER_ID bash -c "cd $1; g++ -o main main.cpp; ./main"
