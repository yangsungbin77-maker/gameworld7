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

## 3단계. 도메인 연결 (완료)

- [x] 도메인 등록업체 확인 → **Namecheap**
- [x] Namecheap 네임서버를 Cloudflare(`molly`/`sid`.ns.cloudflare.com)로 변경 → Active
- [x] 죽은 옛 서버 A 레코드(139.180.136.41) 삭제, 이메일 MX·TXT는 유지
- [x] `gameworld7.com` 을 gameworld7 Worker에 Custom Domain으로 연결
- [x] HTTPS 인증서 자동 발급 확인 (SSL 정상)
- [x] 실제 도메인 접속 확인 → https://gameworld7.com 200 OK (Cloudflare 측 작동, 전 세계 전파는 시차 있음)

## 4단계. 자동 포스팅 워크플로

- [ ] "글 써줘" → Markdown 생성 → build 검증 → push → 자동 게시 흐름 정립
- [ ] (선택) 정기 발행 스케줄 검토

## 5단계. 자매 사이트 복제

- [ ] 같은 틀로 `sportskingdom24.com`(스포츠) 구축
- [ ] 두 번째 도메인 연결

## 애드센스 승인 준비 (2026-10-06)

- [x] 404 페이지 + Cloudflare not_found_handling, 404 noindex·광고 제외
- [x] 개인정보처리방침 재작성(GA4·애드센스·파트너 사이트·EEA 동의·운영자·수정일)
- [x] 소개·운영자 페이지 AI 활용 고지, 필명 '픽셀' 명시
- [x] 홈 상황별 시작 글 안내
- [x] 빌드·내부 링크 검사 통과
- [ ] (운영자) 애드센스 스니펫 복구 시점 결정 — noAds 조건으로 감싸기
- [ ] (운영자) AI가 넣은 경험 문장 13곳 사실 확인 (`adsense-review.md` 5-2)
- [ ] (운영자) CMP 설정, 배포 후 운영 404·ads.txt 응답 확인
