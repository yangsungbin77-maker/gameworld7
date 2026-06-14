# 컨텍스트 노트 — 게임월드7

작업 중 내린 결정과 그 이유를 계속 덧붙인다.

## 2026-06-14 — 프로젝트 시작 배경과 핵심 결정

### 왜 새로 만드는가
- 기존 사이트(`gameworld7.com`, `sportskingdom24.com`)는 워드프레스 + Cloudways 서버로 운영.
- 결제 미납으로 **서버가 완전 삭제(terminate)** 됨. Cloudways 패널 목록에서도 사라짐.
- 백업은 워드프레스 플러그인으로 했으나 외부(구글 드라이브 등) 저장 여부 불확실. 서버 내부에만 있었다면 함께 소실.
- 어차피 "자동 포스팅 블로그"를 만들 계획이었고, 기존 콘텐츠는 SEO 가치가 적어 **새로 시작**하기로 결정.

### 왜 정적 사이트 + Git 인가
- 기존 사고의 본질은 "매달 서버 요금 → 한 번 밀리면 서버째 삭제 → 전부 소실".
- 정적 사이트(Astro) + Git + 무료 호스팅(Cloudflare Pages)으로 가면:
  - 죽을 서버 자체가 없음(다운 불가).
  - Git이 영구 백업 역할 → 같은 사고 원천 차단.
  - 글 작성 = Markdown 파일 추가 후 `git push` → 자동 배포. 자동 포스팅에 가장 적합.
- 사용자가 두 선택지(정적+Git / 워드프레스 재구축) 중 **정적+Git** 선택.

### 환경 관련 결정
- Node.js가 없어 winget으로 설치(v24.16.0).
- 작업 폴더가 한글+공백 경로(`C:\Users\use\클로드 코드`)라 `npm create astro`의 의존성 설치가 실패함.
  → 프로젝트를 **영문 경로 `C:\Users\use\gameworld7`** 에 생성하여 해결. Git 저장소 위치는 한글 폴더일 필요 없음.
- 라이브 미리보기(preview 서버)는 미리보기 도구가 작업 루트(한글 폴더) 밖 경로를 막아 사용 못 함. 대신 `npm run build` 통과로 검증하고, 실제 화면은 배포 후 `*.pages.dev` 주소로 확인하기로 함.

### 블로그 커스터마이징 내용
- `src/consts.ts`: 제목 "게임월드7", 설명 "게임 뉴스 · 공략 · 리뷰...".
- `astro.config.mjs`: `site`를 `https://gameworld7.com`으로.
- 홈(`index.astro`)을 최근 글 목록이 보이도록 재작성, `lang="ko"`.
- 헤더/푸터에서 Astro 기본 소셜 링크 제거, 메뉴 한글화(홈/전체 글/소개).
- 샘플 글 5개 삭제, 첫 글 `welcome.md` 작성.

### 배포 진행 (이어서)
- GitHub 저장소 `yangsungbin77-maker/gameworld7`(공개, main) 생성·push 완료.
- 다음은 Cloudflare Pages에서 이 저장소 연결 → 자동 배포(`*.pages.dev`).

### 도메인
- **등록업체: Namecheap** (gameworld7.com). sportskingdom24.com도 같은 곳일 가능성 높음(미확인).
- 연결 방식: apex 도메인(`gameworld7.com`)을 Pages에 붙이려면 Namecheap의 네임서버를 **Cloudflare 네임서버로 변경**하는 방식이 가장 깔끔(CNAME flattening으로 apex+www 모두 처리). Namecheap은 apex에 CNAME/ALIAS를 안 줘서 네임서버 이전이 사실상 정석.
- **주의:** 네임서버를 Cloudflare로 옮기면 그 도메인의 모든 DNS가 Cloudflare로 넘어감. 만약 이 도메인으로 받는 이메일(MX 레코드)이 있다면 Cloudflare에 다시 추가해야 함. 블로그 도메인이라 이메일은 없을 가능성 높음 — 연결 전 확인 필요.

### 배포 완료 (2026-06-14)
- Cloudflare가 Git 저장소를 Pages가 아닌 **Worker(정적 에셋)** 흐름으로 가져옴. deploy command `npx wrangler deploy`라서 저장소에 `wrangler.jsonc`(name=gameworld7, assets.directory=./dist) 추가하여 해결.
- 라이브 주소: **https://gameworld7.yangsungbin77.workers.dev** (정상 확인).
- Cloudflare ↔ GitHub 연결됨 → `main`에 push하면 자동 재빌드·재배포. "글 쓰면 자동 게시" 파이프라인 작동.
- workers.dev 빌드 Node는 20.x. 빌드/배포 정상.

### 다음 세션이 알아야 할 것
- 다음 할 일: gameworld7.com(Namecheap)을 Cloudflare로 네임서버 이전 → Worker에 Custom Domain 연결. checklist.md 3단계.
- 두 번째 사이트 `sportskingdom24.com`은 이 사이트 완성 후 동일 틀 복제.
