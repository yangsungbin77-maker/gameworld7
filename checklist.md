# 체크리스트 — 게임월드7 정적 블로그 구축

## 1단계. 로컬 구축 (완료)

- [x] Node.js 설치 (v24.16.0)
- [x] Astro 블로그 템플릿 생성 (`C:\Users\use\gameworld7`)
- [x] 게임 블로그로 한글 브랜딩 (제목·메뉴·푸터·홈·소개)
- [x] Astro 기본 소셜 링크(Mastodon/Twitter/GitHub) 제거
- [x] 첫 글 작성 (`welcome.md`)
- [x] `npm run build` 검증 (4페이지 + RSS + 사이트맵)
- [x] Git 초기화 + 첫 커밋, 브랜치 `main`
- [x] 프로젝트 가이드 문서 작성 (CLAUDE.md / checklist.md / context-notes.md)

## 2단계. 배포 (진행 중)

- [x] GitHub 빈 저장소 생성 (`yangsungbin77-maker/gameworld7`)
- [x] 원격 연결 + push (`git push -u origin main`)
- [x] Cloudflare 프로젝트 생성, GitHub 저장소 연결 (Pages가 아닌 **Workers + 정적 에셋** 방식으로 진행, `wrangler.jsonc` 추가)
- [x] 빌드 설정 (build: `npm run build`, deploy: `npx wrangler deploy`)
- [x] 첫 자동 배포 확인 → https://gameworld7.yangsungbin77.workers.dev (정상)
- [x] git push → 자동 재배포 파이프라인 작동 확인

## 3단계. 도메인 연결

- [ ] 도메인 등록업체 확인 (가비아/후이즈/GoDaddy 등)
- [ ] `gameworld7.com` 을 Cloudflare Pages에 연결 (DNS 또는 네임서버 변경)
- [ ] HTTPS 인증서 자동 발급 확인
- [ ] 실제 도메인으로 사이트 접속 확인

## 4단계. 자동 포스팅 워크플로

- [ ] "글 써줘" → Markdown 생성 → build 검증 → push → 자동 게시 흐름 정립
- [ ] (선택) 정기 발행 스케줄 검토

## 5단계. 자매 사이트 복제

- [ ] 같은 틀로 `sportskingdom24.com`(스포츠) 구축
- [ ] 두 번째 도메인 연결
