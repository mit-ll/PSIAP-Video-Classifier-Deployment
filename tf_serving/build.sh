NAME=iva
TAG=latest

for i in "$@"
do
case $i in
    -t=*|--tag=*)
    TAG="${i#*=}"
    shift
    ;;
    -n=*|--name=*)
    NAME="${i#*=}"
    shift
    ;;
    *)
    ;;
esac
done

docker build . --tag="${NAME}:${TAG}"
