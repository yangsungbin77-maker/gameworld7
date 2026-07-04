// Place any global data in this file.
// You can import this data from anywhere in your site by using the `import` keyword.

export const SITE_TITLE = '게임월드7';
export const SITE_DESCRIPTION = '게임 뉴스 · 공략 · 리뷰를 가장 빠르게 전하는 게임 블로그';

// 구글 서치 콘솔 'HTML 태그' 인증의 content 값만 넣는다. 비워두면 메타태그가 출력되지 않는다.
export const GSC_VERIFICATION = '1I9RLg6bwsE0GgOuulefYoYIOUPmDYV4V18ekR4iwuE';

// 네이버 서치어드바이저 'HTML 태그' 인증의 content 값만 넣는다. 비워두면 메타태그가 출력되지 않는다.
export const NAVER_VERIFICATION = '38ab2f323b2b7acf211e5afa0a16ebf533a1f7e3';

// 사이트 내장 미니게임 목록. 홈 그리드와 /games 허브가 함께 사용한다.
export const GAMES = [
	{
		href: '/pang',
		title: '네온 팡',
		emoji: '💎',
		genre: '매치3 퍼즐',
		desc: '같은 보석 3개를 맞춰 터뜨리는 60초 타임어택. 연쇄 콤보가 점수를 불린다.',
		cover: '/images/games/neon-pang.jpg',
	},
	{
		href: '/sachun',
		title: '네온 사천성',
		emoji: '🀄',
		genre: '짝맞추기 퍼즐',
		desc: '같은 그림 둘을 두 번 이하 꺾이는 길로 잇는 클래식 사천성. 힌트·섞기 지원.',
		cover: '/images/games/neon-sachun.jpg',
	},
	{
		href: '/shanghai',
		title: '네온 상하이',
		emoji: '🏯',
		genre: '입체 퍼즐 · 하드',
		desc: '3층으로 쌓인 92블록 입체 사천성. 위가 덮이거나 양옆이 막히면 못 뺀다.',
		cover: '/images/games/neon-shanghai.jpg',
	},
	{
		href: '/maze',
		title: '야옹이 미로 찾기',
		emoji: '😺',
		genre: '키즈',
		desc: '5살도 혼자 OK! 야옹이를 움직여 물고기를 찾는 유아용 미로. 실패 없음, 칭찬만.',
		cover: '/images/games/cat-maze.jpg',
	},
	{
		href: '/snake',
		title: '네온 스네이크',
		emoji: '🐍',
		genre: '아케이드',
		desc: '오브를 먹을수록 길어지고 빨라진다. 벽과 몸통을 피해 최고 기록에 도전.',
		cover: '/images/games/neon-snake.jpg',
	},
	{
		href: '/breakout',
		title: '네온 벽돌깨기',
		emoji: '🧱',
		genre: '아케이드',
		desc: '패들로 공을 튕겨 네온 벽돌을 전부 부수기. 스테이지마다 더 빨라진다.',
		cover: '/images/games/neon-breakout.jpg',
	},
	{
		href: '/game',
		title: '넘버 텐',
		emoji: '🔟',
		genre: '두뇌 퍼즐',
		desc: '드래그로 묶은 숫자 합이 10이면 사라진다. 2분 안에 최고 점수에 도전.',
		cover: '/images/games/number-ten.jpg',
	},
	{
		href: '/memory',
		title: '카드 짝 맞추기',
		emoji: '🃏',
		genre: '기억력',
		desc: '같은 그림 카드 두 장을 찾아 뒤집기. 더 적은 시도, 더 빠른 기록.',
		cover: '/images/games/memory-match.jpg',
	},
];
