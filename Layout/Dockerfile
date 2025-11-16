FROM nginx:alpine

# HTML 파일과 이미지 복사
COPY ourhome_layout_v9.html /usr/share/nginx/html/index.html
COPY ourhome_ci.png /usr/share/nginx/html/ourhome_ci.png

# nginx 기본 설정
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]