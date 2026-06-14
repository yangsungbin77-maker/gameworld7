# 자동 발행 작업 지시서 (게임월드7)

이 문서는 예약 루틴이 **이틀에 한 번** 그대로 따라 실행하는 절차다. 목표는 글 1편 자동 발행 — 각 글에 **외부링크 1개·내부링크 1개·이미지 1개**가 반드시 들어간다.

## 절차 (3단계)

작업 폴더는 이 저장소 루트(`gameworld7`)다. PATH에 node가 없으면 먼저 잡는다.

```
node automation/prepare.mjs
```

1. 위 명령을 실행한다. 출력된 JSON(= `automation/assignment.json`)에 이번 글의 재료가 들어 있다.
   - `topic` — 이번 글 주제
   - `pubDate` — 오늘 날짜(그대로 frontmatter에 넣는다)
   - `heroImage` — 대표 이미지 경로(그대로 frontmatter `heroImage`에 넣는다)
   - `internalLink.url` / `internalLink.title` — 본문에 자연스럽게 걸 **내부링크**
   - `externalLink.url` / `externalLink.label` — 본문에 자연스럽게 걸 **외부링크**

2. `src/content/blog/<영문-slug>.md` 파일을 새로 만들어 글을 쓴다. slug는 주제를 영어로 옮긴 짧은 케밥케이스(예: `co-op-games-for-beginners`). frontmatter는 아래 형식을 지킨다.

   ```markdown
   ---
   title: '글 제목(한국어)'
   description: '한 줄 요약(검색·미리보기 노출)'
   pubDate: '<assignment의 pubDate 그대로>'
   heroImage: '<assignment의 heroImage 그대로>'
   ---

   본문...
   ```

3. 글을 다 쓰면 아래를 실행한다(검증·발행 자동).

   ```
   node automation/finalize.mjs <위에서 정한 slug>
   ```

   이 스크립트가 외부·내부링크와 이미지가 실제로 들어갔는지 확인하고, 빌드가 통과하면 커밋·푸시한다(Cloudflare 자동 배포). 검증 실패 시 멈추므로, 메시지를 읽고 글을 고친 뒤 다시 실행한다.

## 글쓰기 규칙 (반드시 지킬 것)

- **톤**: 존댓말 + 사람 냄새. 게임을 좋아하는 사람이 직접 경험을 풀어주듯 쓴다. 정형화된 "특징/이런 사람에게" 식 라벨 나열은 피한다.
- **한국어 마침표 규칙**: 문장을 콜론(`:`)으로 끝내지 않는다. `.`, `?`, `!`로 끝낸다(코드·키값 라벨 제외).
- **분량**: 본문 600~900자 내외, 소제목(`##`) 2~4개.
- **내부링크 1개**: `[앵커 텍스트](assignment.internalLink.url)` 형태로 문맥에 맞게 1회 삽입. 앵커는 `internalLink.title`을 참고해 자연스럽게.
- **외부링크 1개**: `[앵커 텍스트](assignment.externalLink.url)` 형태로 1회 삽입. 신뢰 출처이므로 "공식 안내", "여기서 확인" 같은 맥락으로 자연스럽게 건다.
- **이미지**: 본문에 따로 넣지 않는다. frontmatter `heroImage`만 지정하면 레이아웃이 상단 배너로 표시한다.
- 과장·허위 정보 금지. 확실하지 않은 수치는 단정하지 않는다.

## 주제가 떨어졌을 때

`automation/prepare.mjs`가 "발행할 주제가 없습니다"로 멈추면, 발행하지 말고 종료한다(빈 글 금지). 주제는 사람이 `automation/topics.md`에 채운다.
