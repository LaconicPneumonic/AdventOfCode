#!/usr/bin/env bash
# check if image exists
# build image otherwise

CONTAINER_NAME="aoc2021"

if [[ ! $(docker images "$CONTAINER_NAME" --format "{{.Repository}}" ) || $2 = "build" ]]; then
    echo "building container"
    docker build . -f DOCKERFILE -t $CONTAINER_NAME
fi

# cp stuff in there

CONTAINER_ID=$(docker ps --filter "name=$CONTAINER_NAME" --format "{{.ID}}")

if [[  -z "$CONTAINER_ID" || $2 = "build" ]];
then
    echo "RUNNING CONTAINER"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
    docker run -dit --name $CONTAINER_NAME $CONTAINER_NAME bash
    CONTAINER_ID=$(docker ps --filter "name=$CONTAINER_NAME" --format "{{.ID}}")
    echo "CONTAINER ID IS $CONTAINER_ID"

fi

docker start $CONTAINER_ID


# execute the command!
docker cp $1/ $CONTAINER_ID:/usr/src/aoc

echo "RUNNING"
echo "-------"

if [[ $2 = "test" ]];
then
    docker exec $CONTAINER_ID bash -c "cd $1; g++ -o main main.cpp &&  valgrind --leak-check=yes ./main"
else
    docker exec $CONTAINER_ID bash -c "cd $1; g++ -o main main.cpp && ./main"
fi
