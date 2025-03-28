#!/bin/bash

set -e


AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
AWS_REGION=${AWS_REGION:-us-east-1}
REPO_NAME=my-ecr-repository
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME"
APPS=("app1" "app2")


echo "🔐 Haciendo login en ECR..."
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_URI"

for APP in "${APPS[@]}"; do
  IMAGE_TAG="$APP" 

  echo "📦 Procesando $APP..."

  echo "🐳 Construyendo imagen $REPO_NAME:$IMAGE_TAG..."
  docker build -t "$REPO_NAME:$IMAGE_TAG" "../apps/$APP"

  docker tag "$REPO_NAME:$IMAGE_TAG" "$ECR_URI:$IMAGE_TAG"
  echo "🚀 Subiendo imagen como $ECR_URI:$IMAGE_TAG..."
  docker push "$ECR_URI:$IMAGE_TAG"

  echo "✅ Imagen $APP subida como $ECR_URI:$IMAGE_TAG"
done