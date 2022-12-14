#!/bin/sh

mkdir data
mkdir data/extracted
mkdir data/cache
mkdir data/compressed
mkdir user
cp example_config.json user/config.json
curl 'https://download.wetransfer.com/eugv/7c8e1f8f8c29358da02e2c60f15c960120221213153557/860e8fbc0678b4f28faa4a5a64cee6068cb37078/rotten_tomatoes.zip?token=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NzA5NDU3NzMsImV4cCI6MTY3MDk0NjM3MywidW5pcXVlIjoiN2M4ZTFmOGY4YzI5MzU4ZGEwMmUyYzYwZjE1Yzk2MDEyMDIyMTIxMzE1MzU1NyIsImZpbGVuYW1lIjoicm90dGVuX3RvbWF0b2VzLnppcCIsIndheWJpbGxfdXJsIjoiaHR0cDovL3N0b3JtLWludGVybmFsLnNlcnZpY2UuZXUtd2VzdC0xLndldHJhbnNmZXIubmV0L2FwaS93YXliaWxscz9zaWduZWRfd2F5YmlsbF9pZD1leUpmY21GcGJITWlPbnNpYldWemMyRm5aU0k2SWtKQmFITkxkMmxtTUU4d2FrRm5RVDBpTENKbGVIQWlPaUl5TURJeUxURXlMVEV6VkRFMU9qUTJPakV6TGpBd01Gb2lMQ0p3ZFhJaU9pSjNZWGxpYVd4c1gybGtJbjE5LS1iY2U3YTVjMmU2ZDliMWI3MDI4YjZlMjkzYzRlZGUwYjFjOTVlYTVkOGVlNGI3MWI2ODlhMzk1YTkwMzFkYTc4IiwiZmluZ2VycHJpbnQiOiI4NjBlOGZiYzA2NzhiNGYyOGZhYTRhNWE2NGNlZTYwNjhjYjM3MDc4IiwiY2FsbGJhY2siOiJ7XCJmb3JtZGF0YVwiOntcImFjdGlvblwiOlwiaHR0cDovL2Zyb250ZW5kLnNlcnZpY2UuZXUtd2VzdC0xLndldHJhbnNmZXIubmV0L3dlYmhvb2tzL2JhY2tlbmRcIn0sXCJmb3JtXCI6e1widHJhbnNmZXJfaWRcIjpcIjdjOGUxZjhmOGMyOTM1OGRhMDJlMmM2MGYxNWM5NjAxMjAyMjEyMTMxNTM1NTdcIixcImRvd25sb2FkX2lkXCI6MTczNDMwMzU5MTR9fSJ9.kkxtevzeqOw-O8W_OL2DEhLccNp9iR-w0Iv7ThRDo-s&cf=y' --location --output data/compressed/rotten_tomatoes.zip
unzip data/compressed/rotten_tomatoes.zip
mv rotten_tomatoes*.csv data/extracted
