#!/bin/bash

echo "📦 변경 파일 추가 중..."
git add .

echo "📝 커밋 메시지를 입력하세요:"
read msg

echo "✅ 커밋 중..."
git commit -m "$msg"

echo "🚀 GitHub로 푸시 중..."
git push

echo "🌐 Render 수동 배포 시작..."
curl -X POST "https://api.render.com/deploy/srv-cvqbaqjipnbc73cokr7g?key=h39iGviZBRU"

echo "🎉 완료되었습니다!"
