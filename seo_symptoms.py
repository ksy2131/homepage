# -*- coding: utf-8 -*-
# 증상별 안내 데이터 + 동네·지역 × 증상 페이지 — build_site.py 안에서 exec로 불러 씀
# 문장 안의 {n} 은 동네·지역 이름으로 바뀝니다.

SYMPTOMS = [
 {"slug": "breaker", "name": "차단기 내려감", "short": "차단기",
  "kws": ["차단기 내려감", "차단기 자꾸 떨어짐", "두꺼비집 내려감", "차단기 수리", "차단기 교체"],
  "lead": "{n}에서 차단기가 자꾸 내려가거나, 올려도 바로 다시 떨어진다면 원인을 찾아야 하는 신호입니다. 어떤 차단기가 떨어졌는지만 알아도 원인의 절반은 좁혀집니다.",
  "match": ["차단기", "트립"], "svc": "home-repair", "guide": "guide-breaker-trips", "diags": ["which", "reset", "chart"],
  "causes": [("누전", "시험버튼 있는 누전차단기가 떨어짐. 비 오는 날·세탁기·정수기 쓸 때 잦음", "절연저항 측정으로 새는 회로·기기를 찾아 정비"),
             ("과부하", "인덕션·에어컨·히터를 같이 켤 때 분기차단기가 떨어짐", "전용 회로 증설, 회로 분리"),
             ("콘센트·접속부 불량", "특정 콘센트를 쓸 때만 떨어지고 그 주변이 뜨거움", "콘센트 교체, 접속부 재시공"),
             ("차단기 노후", "손잡이가 헐겁고 정상 사용에도 떨어짐", "같은 용량 차단기로 교체")],
  "selfcheck": ["분전반을 열어 떨어진 차단기가 큰 누전차단기인지, 작은 분기차단기인지 확인합니다.",
                "떨어진 회로에 꽂힌 플러그를 모두 뽑고 차단기를 한 번만 올려 봅니다.",
                "버티면 기기를 하나씩 꽂으며 어느 기기에서 떨어지는지 봅니다.",
                "플러그를 다 뽑아도 바로 떨어지면 배선·콘센트 쪽이니 더 올리지 말고 전화 주세요."],
  "dont": ["차단기를 테이프·끈으로 고정해 못 떨어지게 하기", "20A 차단기를 30A로 임의로 키우기 (전선은 그대로라 벽 속 전선이 과열됩니다)", "젖은 손으로 분전반 만지기"],
  "onsite": ["떨어진 차단기 종류와 회로 확인", "회로별 사용 전류 측정 (과부하 여부)", "절연저항 측정 (누전 여부·위치)", "콘센트·접속부 발열 확인", "원인 회로만 정비하고 나머지는 그대로 둠"],
  "faq": [("{n} 차단기가 계속 내려가는데 오늘 와주실 수 있나요?", "전화로 증상을 먼저 듣고 가능한 가장 빠른 시간으로 방문 일정을 잡습니다. 타는 냄새가 나면 그 차단기를 내려 두고 기다려 주세요."),
          ("차단기만 새 것으로 바꾸면 해결되나요?", "차단기 노후가 원인일 때만 그렇습니다. 누전이나 과부하가 원인이면 차단기를 바꿔도 다시 떨어집니다. 원인부터 측정으로 확인합니다."),
          ("인덕션을 켜면 차단기가 떨어지는데 왜 그런가요?", "인덕션은 3kW가 넘는 큰 가전이라 다른 주방 가전과 한 회로를 쓰면 한계를 넘습니다. 인덕션 전용 회로를 따로 빼는 것이 정답입니다."),
          ("비 오는 날에만 차단기가 떨어지는 이유는요?", "베란다·실외기·외부 콘센트 쪽으로 습기가 들어가 누전이 생기는 경우가 많습니다. 맑은 날엔 멀쩡해도 절연이 약해진 상태입니다."),
          ("차단기가 아예 안 올라가요.", "올리는 순간 바로 떨어지면 그 회로에 지금 문제가 있는 상태입니다. 여러 번 시도하지 말고 전화 주세요.")]},

 {"slug": "leak", "name": "누전", "short": "누전",
  "kws": ["누전", "누전 수리", "누전 탐지", "누전 점검", "누전차단기"],
  "lead": "{n}에서 누전차단기가 떨어지거나 가전을 만질 때 찌릿하다면 전기가 정해진 길 밖으로 새고 있는 것입니다. 누전은 감전과 화재로 이어질 수 있어 위치를 찾아 고쳐야 합니다.",
  "match": ["누전", "절연", "ELB"], "svc": "home-repair", "guide": "guide-leakage-check", "diags": ["flow", "which"],
  "causes": [("습기", "욕실·베란다·주방 싱크대 하부 콘센트, 실외기 배선", "젖은 구간 배선·콘센트 교체, 방수 처리"),
             ("가전제품", "세탁기·정수기·전기온수기·오래된 냉장고", "기기를 하나씩 분리해 측정, 문제 기기 확인"),
             ("배선 손상", "못·타공으로 벽 속 전선 피복 손상, 오래된 배선", "구간별 절연저항 측정 후 해당 구간 교체"),
             ("누수", "윗집 누수로 천장 조명·배선에 물이 듦", "등기구·배선 정비, 누수 수리 일정과 맞춤")],
  "selfcheck": ["시험버튼이 있는 누전차단기가 떨어졌는지 확인합니다.",
                "세탁기·정수기·전기온수기처럼 물 쓰는 기기 플러그를 먼저 뽑고 올려 봅니다.",
                "버티면 기기를 하나씩 다시 꽂아 어느 기기에서 떨어지는지 확인합니다.",
                "다 뽑아도 떨어지면 배선 쪽이라 측정 장비가 필요합니다."],
  "dont": ["누전차단기를 일반 차단기로 바꾸기", "물기 있는 손으로 콘센트·분전반 만지기", "찌릿한 기기를 계속 쓰기"],
  "onsite": ["회로별 절연저항 측정", "회로 안에서 구간을 나눠 다시 측정해 위치 좁히기", "콘센트·접속부·기기 하나씩 분리 확인", "원인 구간만 교체·정비", "정비 후 절연저항 재측정으로 확인"],
  "faq": [("{n} 누전 위치를 못 찾으면 어떻게 되나요?", "절연저항계로 회로별, 구간별로 나눠 측정하면 대부분 위치가 좁혀집니다. 작업 전에 점검 범위와 비용을 먼저 말씀드립니다."),
          ("누전차단기 시험버튼은 왜 있나요?", "누전차단기가 제대로 동작하는지 확인하는 버튼입니다. 눌러서 떨어지면 정상이고, 안 떨어지면 차단기 교체가 필요합니다."),
          ("가전을 만질 때 찌릿한데 괜찮을까요?", "그 기기나 콘센트로 전기가 새고 있다는 신호입니다. 바로 플러그를 뽑고 사용을 멈춰 주세요."),
          ("윗집에서 물이 샌 뒤로 누전이 생겼어요.", "천장 등기구나 배선에 물이 들어간 경우가 많습니다. 누수 수리와 도배 일정에 맞춰 전기 정비를 같이 잡으면 두 번 일하지 않습니다."),
          ("누전은 고치는 데 오래 걸리나요?", "위치를 찾는 데 시간이 걸리고, 찾고 나면 정비는 대부분 금방 끝납니다.")]},

 {"slug": "outlet", "name": "콘센트 탄냄새", "short": "콘센트",
  "kws": ["콘센트 탄냄새", "콘센트 그을림", "콘센트 교체", "콘센트 뜨거움", "콘센트 증설"],
  "lead": "{n}에서 콘센트가 뜨겁거나 검게 그을렸거나, 플라스틱 타는 냄새가 난다면 그 콘센트 안에서 열이 나고 있는 것입니다. 화재로 번지기 전에 교체해야 합니다.",
  "match": ["콘센트"], "svc": "home-repair", "guide": "guide-outlet-burn", "diags": ["chart"],
  "causes": [("접촉 불량", "플러그가 헐겁게 꽂히고 꽂은 부분이 뜨거움", "콘센트 교체"),
             ("과부하", "멀티탭에 히터·드라이어·전기포트를 같이 꽂음", "기기 분산, 필요하면 콘센트·회로 증설"),
             ("접속부 풀림", "콘센트 뒤 전선 연결부가 느슨해져 발열", "접속부 재시공 후 콘센트 교체"),
             ("습기·누전", "싱크대 하부·욕실 근처 콘센트 그을림", "방수형 콘센트로 교체, 배선 점검")],
  "selfcheck": ["타는 냄새가 나는 콘센트의 플러그를 바로 뽑습니다.", "그 콘센트가 연결된 차단기를 내립니다.",
                "멀티탭에 큰 가전 여러 개가 꽂혀 있었는지 확인합니다.", "사진을 찍어 문자로 보내 주시면 교체 범위를 먼저 안내합니다."],
  "dont": ["그을린 콘센트를 닦아서 다시 쓰기", "멀티탭에 멀티탭을 연결하기", "녹은 플러그를 계속 꽂아 쓰기"],
  "onsite": ["콘센트 커버를 열어 뒤쪽 전선·접속부 확인", "같은 회로 다른 콘센트 발열 확인", "회로 사용 전류 측정", "콘센트 교체, 필요하면 전용 콘센트·회로 증설", "교체 후 전압·발열 확인"],
  "faq": [("{n} 콘센트 하나만 바꿔도 와주시나요?", "네. 콘센트 한 개 교체도 출장합니다. 같은 김에 다른 콘센트 상태도 봐 드립니다."),
          ("그을린 콘센트, 겉만 깨끗하면 써도 되나요?", "안 됩니다. 그을림은 안쪽 접점이 이미 열로 상한 흔적이라 교체해야 합니다."),
          ("콘센트를 더 늘릴 수 있나요?", "벽 속 배관과 회로 상태를 보고 콘센트 증설이나 전용 콘센트를 추가할 수 있습니다."),
          ("주방 콘센트만 자꾸 타요.", "주방은 전기를 많이 쓰는 가전이 몰리고 물도 가까워 탈이 잘 납니다. 인덕션·식기세척기 같은 큰 가전은 전용 회로로 분리하는 것이 좋습니다."),
          ("콘센트에서 찌직 소리가 나요.", "안에서 불꽃이 튀는 소리일 수 있습니다. 차단기를 내리고 쓰지 마세요.")]},

 {"slug": "light", "name": "전등 안켜짐", "short": "전등",
  "kws": ["전등 안켜짐", "LED 방등 교체", "방등 깜빡임", "거실등 교체", "조명 교체"],
  "lead": "{n}에서 방등·거실등이 깜빡이거나 켜지지 않는다면 LED 모듈·안정기 수명이거나 스위치·배선 접촉 문제인 경우가 대부분입니다. 어디가 문제인지에 따라 부품만 바꿀지 등 전체를 바꿀지가 갈립니다.",
  "match": ["LED", "방등", "등기구", "식탁등", "조명", "스위치", "가로등"], "svc": "home-repair", "guide": "guide-led-light", "diags": [],
  "causes": [("LED 모듈 수명", "일부만 어둡거나 한쪽만 켜짐", "모듈 교체 또는 등기구 교체"),
             ("안정기(컨버터) 고장", "깜빡이다가 아예 안 켜짐", "안정기 교체, 오래됐으면 등기구 교체"),
             ("스위치 불량", "스위치를 여러 번 눌러야 켜짐, 스위치가 뜨거움", "스위치 교체"),
             ("천장 배선·누수", "윗집 누수 후 고장, 등 안쪽 부식", "배선 정비 후 등기구 교체")],
  "selfcheck": ["같은 방 다른 등, 다른 방 등은 켜지는지 봅니다.", "스위치를 껐다 켤 때 반응이 있는지 확인합니다.",
                "등 커버 안쪽에 물 자국·녹이 있는지 봅니다 (차단기 내리고 확인).", "등 크기와 형태를 사진으로 보내 주시면 맞는 등을 준비해 갑니다."],
  "dont": ["차단기를 올린 채 천장 등 만지기", "의자 위에서 혼자 무리하게 작업하기", "누수 자국 있는 등을 그대로 쓰기"],
  "onsite": ["스위치·천장 배선 전압 확인", "모듈·안정기 상태 확인", "부품 교체와 등기구 교체 중 맞는 쪽 안내", "기존 브래킷 재사용 여부 확인", "교체 후 점등·밝기 확인"],
  "faq": [("{n} 방등 하나만 교체해도 오시나요?", "네. 방등 한 개도 출장합니다. 크기 맞춰 등을 준비해 가려면 사진을 먼저 보내 주세요."),
          ("모듈만 바꾸는 게 싼가요, 등 전체가 나은가요?", "등기구가 오래됐거나 다른 등도 같은 시기에 달았다면 전체 교체가 오래 씁니다. 상태를 보고 두 가지를 비교해 말씀드립니다."),
          ("등을 바꿨는데도 안 켜져요.", "스위치나 천장 배선 연결부 문제일 수 있습니다. 전압을 재 보면 바로 구분됩니다."),
          ("스마트 스위치가 앱에서 안 돼요.", "스위치 자체 통신부 고장이 많습니다. 같은 기종이나 호환 스위치로 교체합니다."),
          ("형광등을 LED로 바꾸면 전기요금이 줄어드나요?", "같은 밝기 기준으로 LED가 전기를 덜 씁니다. 오래된 형광등 안정기는 고장도 잦아 교체를 많이 하십니다.")]},

 {"slug": "panel", "name": "분전반 교체", "short": "분전반",
  "kws": ["분전반 교체", "두꺼비집 교체", "분전반 공사", "차단기 교체", "회로 증설"],
  "lead": "{n}에서 분전반(두꺼비집)이 오래돼 차단기가 헐겁거나 변색됐다면, 또는 인덕션·에어컨을 새로 들이며 회로가 모자라다면 분전반 교체나 회로 증설을 검토할 때입니다.",
  "match": ["분전반", "차단기 교체", "메인 차단기", "메인차단기", "회로"], "svc": "panel", "guide": "guide-panel-replace", "diags": ["flow", "chart"],
  "causes": [("노후", "입주 15년 이상, 차단기 손잡이 헐거움·변색", "분전반 전체 교체"),
             ("회로 부족", "인덕션·식기세척기·시스템 에어컨 추가", "분기차단기·전용 회로 증설"),
             ("과열 흔적", "분전반 안 단자 변색, 열기", "단자 재체결, 손상 차단기 교체"),
             ("회로 표시 없음", "어느 차단기가 어느 방인지 모름", "교체 후 회로 이름표 부착")],
  "selfcheck": ["분전반 문을 열어 차단기 개수와 상태(변색·헐거움)를 봅니다.", "차단기에 방 이름표가 붙어 있는지 확인합니다.",
                "새로 들일 큰 가전(인덕션·건조기·에어컨)이 있는지 정리합니다.", "분전반 전체가 나오게 사진을 찍어 보내 주시면 견적이 빨라집니다."],
  "dont": ["분전반 덮개를 연 채 손대기", "차단기 용량을 임의로 키우기", "분전반 앞을 짐으로 막아 두기"],
  "onsite": ["기존 회로·용량 확인", "사용 가전 기준으로 필요한 회로 수 산정", "전기 차단 시간 미리 안내", "분전반·차단기 교체와 회로 정리", "회로 이름표 부착, 절연·전압 측정"],
  "faq": [("{n} 분전반 교체는 얼마나 걸리나요?", "일반 세대는 대부분 반나절 안에 끝나고, 그동안 전기가 잠시 끊깁니다. 정확한 시간은 현장을 보고 미리 말씀드립니다."),
          ("인덕션만 쓰려는데 분전반을 다 바꿔야 하나요?", "분전반에 빈 자리가 있으면 인덕션 전용 차단기와 회로만 추가하면 됩니다. 자리가 없거나 너무 낡았을 때 교체를 권합니다."),
          ("교체 후 차단기 이름표도 붙여 주시나요?", "네. 회로마다 어느 공간인지 표시해 드려 다음에 문제가 생겨도 바로 찾을 수 있습니다."),
          ("상가 분전반도 하시나요?", "네. 상가·사무실·매장 분전반 교체와 회로 증설도 합니다."),
          ("계량기함 메인차단기도 교체하나요?", "네. 복도 계량기함의 세대 메인차단기 교체도 합니다. 타는 냄새가 나면 바로 연락 주세요."),
          ("전기 용량 자체가 부족하면 어떻게 하나요?", "한전 증설 신청부터 인입선·분전반 공사까지 함께 진행합니다.")]},

 {"slug": "outage", "name": "전기 안들어옴", "short": "정전",
  "kws": ["집 전기 안들어옴", "세대 정전", "전기 나감", "메인차단기 교체", "계량기함 차단기"],
  "lead": "{n}에서 우리 집만 전기가 다 나갔다면 집 안 분전반이 아니라 복도 계량기함의 메인차단기 문제일 수 있습니다. 어디까지 전기가 나갔는지부터 확인하면 원인이 빨리 좁혀집니다.",
  "match": ["정전", "전기 안 들어옴", "메인 차단기", "메인차단기"], "svc": "home-repair", "guide": "guide-power-out", "diags": ["flow", "which"],
  "causes": [("계량기함 메인차단기", "집 안 분전반은 멀쩡한데 전체가 꺼짐", "메인차단기 점검·교체"),
             ("누전차단기 동작", "집 안 분전반의 큰 차단기가 내려가 있음", "누전 원인 찾아 정비 후 복구"),
             ("단자 과열", "계량기함·분전반에서 타는 냄새", "손상 단자·차단기 교체"),
             ("단지·지역 정전", "옆집·복도등도 같이 꺼짐", "관리사무소·한전 확인")],
  "selfcheck": ["옆집·복도 조명도 꺼졌는지 확인합니다 (같이 꺼졌으면 단지·지역 정전).", "집 안 분전반의 큰 차단기가 내려갔는지 봅니다.",
                "집 안이 멀쩡하면 복도 계량기함의 우리 집 메인차단기를 확인합니다.", "타는 냄새가 나면 아무것도 올리지 말고 바로 전화 주세요."],
  "dont": ["타는 냄새 나는 차단기를 반복해서 올리기", "계량기함 안 전선 만지기", "정전 중 전열기구 플러그를 꽂아 둔 채 복구하기"],
  "onsite": ["단지·세대 정전 구분", "계량기함 메인차단기와 단자 상태 확인", "세대 분전반·누전 여부 측정", "손상 차단기·단자 교체", "복구 후 전압 측정과 세대 사용 확인"],
  "faq": [("{n} 아파트인데 우리 집만 전기가 나갔어요.", "복도 계량기함 안 세대 메인차단기를 먼저 확인해 보세요. 내려가 있거나 타는 냄새가 나면 연락 주시면 바로 봐 드립니다."),
          ("메인차단기는 관리사무소가 고치나요?", "세대 메인차단기는 보통 세대 부담인 경우가 많습니다. 관리사무소에 확인하시고, 필요하면 저희가 교체합니다."),
          ("정전 후 일부 콘센트만 안 돼요.", "복구 과정에서 분기차단기 하나가 내려가 있거나 그 회로에 문제가 남은 경우입니다."),
          ("밤에 전기가 나갔는데 어떻게 하나요?", "냄새·연기가 없으면 차단기를 한 번만 올려 보시고, 다시 떨어지면 내려 둔 채로 연락 주세요."),
          ("정전이 자주 반복돼요.", "메인차단기 노후나 단자 접촉 불량, 세대 과부하일 수 있어 측정으로 확인해야 합니다.")]},
]
SYM = {s["slug"]: s for s in SYMPTOMS}

# 동네 성격(신축/혼합/노후)에 따라 달라지는 문장 — 같은 증상이라도 동네마다 다른 내용
AREA_TYPE = {"yangju-okjeong": "신축", "yangju-hoecheon": "신축", "yangju-deokjeong": "혼합", "uijeongbu-minrak": "신축",
             "uijeongbu-gosan": "신축", "uijeongbu-singok": "노후", "hanam-misa": "신축", "hanam-gamil": "신축",
             "uijeongbu": "혼합", "yangju": "신축", "pocheon": "혼합", "dongducheon": "노후", "namyangju": "혼합", "guri": "혼합",
             "hanam": "신축", "nowon": "노후", "dobong": "노후", "gangbuk": "노후", "seongbuk": "혼합"}
TYPE_NOTE = {
 "신축": {"breaker": "{n}처럼 입주한 지 오래되지 않은 단지는 차단기 자체보다 입주 후 새로 들인 인덕션·식기세척기·건조기로 주방 회로가 과부하되는 경우가 가장 많습니다. 싱크대 하부 콘센트 누전도 자주 봅니다.",
          "leak": "{n} 신축 단지에서는 싱크대 하부·아일랜드 식탁 콘센트처럼 물과 가까운 곳, 그리고 윗집 누수 뒤 천장 등기구 쪽 누전을 자주 만납니다.",
          "outlet": "{n} 신축 세대는 콘센트 자체보다 멀티탭에 큰 가전을 몰아 꽂아 생기는 발열, 아일랜드 식탁처럼 바닥·가구에 붙은 콘센트의 습기 문제가 많습니다.",
          "light": "{n} 신축 단지는 입주 때 달린 LED 방등의 모듈·안정기가 몇 년 지나 하나둘 고장 나기 시작하는 시기입니다. 스마트 스위치 통신 불량도 종종 있습니다.",
          "panel": "{n} 신축 세대는 분전반 교체보다 인덕션·시스템 에어컨 전용 회로 증설 문의가 대부분입니다. 분전반 빈 자리를 활용하면 공사가 간단합니다.",
          "outage": "{n} 아파트는 복도 계량기함에 세대 메인차단기가 따로 있어, 집 안 분전반이 멀쩡한데 전체가 꺼졌다면 계량기함부터 봅니다."},
 "혼합": {"breaker": "{n}은 오래된 단지와 새 단지가 섞여 있어 원인도 갈립니다. 오래된 집은 차단기 노후와 콘센트 접속부, 새 집은 주방 가전 과부하가 많습니다.",
          "leak": "{n}의 오래된 주택·빌라는 벽 속 배선 노후, 새 단지는 주방·욕실 콘센트 습기 쪽 누전이 많습니다.",
          "outlet": "{n}의 오래된 건물은 콘센트 접점이 닳아 플러그가 헐거워진 경우가, 새 건물은 멀티탭 과부하가 많습니다.",
          "light": "{n}에서는 오래된 형광등을 LED로 바꾸는 교체와, 새 단지 LED 방등 모듈 고장 수리가 함께 많습니다.",
          "panel": "{n}의 오래된 집은 분전반 전체 교체, 새 집은 전용 회로 증설 위주로 진행합니다.",
          "outage": "{n}은 아파트는 계량기함 메인차단기, 주택·상가는 인입구 차단기와 분전반부터 확인합니다."},
 "노후": {"breaker": "{n}처럼 지은 지 오래된 아파트·빌라가 많은 곳은 차단기 노후와 콘센트 뒤 접속부 풀림이 원인인 경우가 많습니다. 차단기 손잡이가 헐겁다면 교체 시기입니다.",
          "leak": "{n}의 오래된 건물은 벽 속 배선 피복이 약해져 생기는 누전이 많아, 구간을 나눠 측정해 위치를 찾습니다.",
          "outlet": "{n}의 오래된 집은 콘센트 접점이 닳아 플러그가 헐겁게 꽂히면서 열이 나는 경우가 대부분입니다. 집 전체 콘센트를 한 번에 바꾸는 경우도 많습니다.",
          "light": "{n}에서는 오래된 형광등과 안정기를 LED 등기구로 바꾸는 교체 문의가 가장 많습니다.",
          "panel": "{n}처럼 입주 15~20년이 넘은 집은 분전반·차단기 노후로 교체를 권하는 경우가 많습니다. 교체하면서 주방·에어컨 회로를 나누면 차단기 떨어짐도 같이 해결됩니다.",
          "outage": "{n}의 오래된 건물은 메인차단기와 단자 노후로 전체 정전이 생기는 경우가 있어, 단자 상태까지 확인합니다."}}

def sym_text(t, n):
    return t.replace("{n}", n)

def related_posts(sym, scope_match=None, region=None, limit=6):
    def hit_sym(x):
        s = (x["title"] + " " + " ".join(x.get("body") or []))
        return any(m in s for m in sym["match"])
    def hit_scope(x):
        if scope_match: return any(m in (x.get("location") or "") + x["title"] for m in scope_match)
        if region: return x["region"] == region
        return True
    a = [x for x in POSTS if hit_scope(x) and hit_sym(x)]
    c = [x for x in POSTS if hit_scope(x) and x not in a]
    b = [x for x in POSTS if hit_sym(x) and x not in a and x not in c]
    return (a + c + b)[:limit], len(a) + len(c)

def case_story_html(posts, n_kw, sym, limit=2):
    """실제 시공사례 본문 일부를 '이 동네에서 실제로 있었던 일'로 보여줌 — 페이지마다 다른 실제 내용"""
    out = []
    for x in posts[:limit]:
        paras = [t for t in (x.get("body") or []) if not t.startswith("## ") and not t.lstrip().startswith("- ")][:2]
        if not paras: paras = [x["summary"]]
        img = f'<img src="{E(x["photos"][0])}" alt="{E(x.get("location") or x["region"])} {E(x["title"])}" loading="lazy">' if x.get("photos") else ""
        out.append(f'<div class="story">{img}<div><span class="case-r">{E(x.get("location") or x["region"])} · {E(x["date"])}</span><h3>{E(x["title"])}</h3>'
                   + "".join(f"<p>{E(t)}</p>" for t in paras) + f'<a class="link" href="case-{x["slug"]}.html">현장 기록 전체 보기 →</a></div></div>')
    return "".join(out)

def area_list_html(base_slug, n_kw, sym):
    rg = next((x for x in REGIONS if x["slug"] == base_slug), None)
    if not rg: return ""
    dongs = rg.get("dongs") or rg["areas"]
    locs = [l for l in LOCALS if l["region"] == base_slug and sym_built(l["slug"])]
    loc_html = "".join(f'<li><a class="link" href="{symptom_page_slug(l["slug"], sym)}.html">{E(l["kn"])} {E(sym["name"])}</a> — {E(l["intro"].split(".")[0])}.</li>' for l in locs)
    return (f'<h2>{E(n_kw)} 어느 동네든 갑니다</h2><p>{E(rg["intro"])}</p>'
            f'<p>{E(n_kw)} {E(", ".join(dongs))} 어디서든 {E(sym["name"])} 문제로 연락 주시면 출장합니다.</p>'
            + (f'<h3>{E(n_kw)} 동네별 {E(sym["name"])} 안내</h3><ul class="dots">{loc_html}</ul>' if loc_html else ""))

def symptom_page_slug(base_slug, sym):
    return f"{base_slug}-{sym['slug']}"

SYMPTOM_PAGES = []  # 사이트맵용 (slug, priority)

def build_symptom_page(base_slug, n_kw, full, crumbs, region, near, intro, scope_match=None):
    """동네 또는 지역 하나 × 증상 6개 페이지"""
    rg = next((x for x in REGIONS if x["name"] == region), None)
    ty = AREA_TYPE.get(base_slug, "혼합")
    for sym in SYMPTOMS:
        slug = symptom_page_slug(base_slug, sym)
        h1 = f"{n_kw} {sym['name']}"
        posts, local_hits = related_posts(sym, scope_match, region)
        title = f"{n_kw} {sym['name']} | {full} {sym['kws'][1]}·{sym['kws'][2]} 출장 - {C['name']}"
        desc = f"{n_kw} {sym['name']}, {', '.join(n_kw + ' ' + k for k in sym['kws'][1:4])}. 원인 찾는 순서와 집에서 확인할 것, 실제 {region} 시공사례. {C['name']} {C['phone']}"
        kw = ", ".join([f"{n_kw} {k}" for k in sym["kws"]] + [f"{n_kw}{k.replace(' ','')}" for k in sym["kws"][:2]] + [f"{d} {sym['kws'][0]}" for d in near[:4]] + [f"{region} {sym['kws'][0]}"])
        is_local = scope_match is not None
        base_faq = [(sym_text(q, n_kw), sym_text(a, n_kw)) for q, a in sym["faq"]]
        k = sum(map(ord, base_slug)) % len(base_faq)
        faqs = [base_faq[0]] + ([base_faq[1 + k % (len(base_faq) - 1)]] if is_local else base_faq[1:])
        for x in ([p for p in posts if any(m in (p.get("location") or "") + p["title"] for m in scope_match)][:3] if is_local else []):
            faqs.append((f"{n_kw}에서 '{x['title'].split(' – ')[0]}' 같은 경우도 해결하셨나요?",
                         f"네. {x['date'][:7].replace('-', '년 ')}월 {x.get('location') or x['region']} 현장에서 직접 작업했습니다. {x['summary']}"))
        faqs.append((f"{n_kw} 말고 근처 동네도 오시나요?", f"{', '.join(near)} 등 {region} 인근 어디든 출장합니다. 양주에 있어 경기 북부 이동이 빠릅니다."))
        causes = table_html(["원인", "이런 경우", "해결 방법"], sym["causes"])
        diags = "".join(DIAGRAMS[d]() for d in sym["diags"])
        selfc = "".join(f"<li>{E(t)}</li>" for t in sym["selfcheck"])
        dont = "".join(f"<li>{E(t)}</li>" for t in sym["dont"])
        onsite = "".join(f"<li>{icon('check')}{E(t)}</li>" for t in sym["onsite"])
        g = next((x for x in GUIDES if x["slug"] == sym["guide"]), None)
        guide_link = f'<p class="g-more"><a class="link" href="{g["slug"]}.html">더 자세히: {E(g["q"])} →</a></p>' if g else ""
        svc = SVC.get(sym["svc"])
        case_title = f"{n_kw} 근처 실제 시공사례" if local_hits else f"{region} 실제 시공사례"
        case_sec = (f'<section class="sec alt"><div class="wrap"><h2>{E(case_title)}</h2><p class="sub">스마일일렉이 직접 작업한 현장입니다.</p>'
                    f'<div class="cases">{"".join(post_card(x) for x in posts)}</div></div></section>') if posts else ""
        other_sym = "".join(f'<a class="chip" href="{symptom_page_slug(base_slug, s)}.html">{E(n_kw)} {E(s["name"])}</a>' for s in SYMPTOMS if s is not sym)
        near_links = "".join(f'<a class="chip" href="{x[0]}.html">{E(x[1])} {E(sym["name"])}</a>' for x in near_pages(base_slug, sym))
        tags = "".join(f'<span class="tag">#{E((n_kw + k).replace(" ", ""))}</span>' for k in sym["kws"])
        crumb_html = " › ".join([f'<a href="index.html">홈</a>'] + [f'<a href="{p}">{E(t)}</a>' for t, p in crumbs] + [E(sym["name"])])
        sch = [business_schema([full]), faq_schema(faqs),
               crumbs_schema([("홈", "")] + crumbs + [(h1, f"{slug}.html")]),
               howto_schema(f"{n_kw} {sym['name']} 확인 순서", [(f"{i+1}단계", t) for i, t in enumerate(sym["selfcheck"])], sym_text(sym["lead"], n_kw)),
               {"@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": sym["kws"][0],
                "provider": {"@type": "Electrician", "name": C["name"], "telephone": C["phone"]}, "areaServed": {"@type": "Place", "name": full}}]
        page = head(title, desc, f"{slug}.html", kw, sch) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb">{crumb_html}</nav>
  <h1><em>{E(n_kw)}</em> {E(sym['name'])}</h1>
  <p class="lead">{E(sym_text(sym['lead'], n_kw))}</p>
  <div class="hero-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} {E(n_kw)} 출장 상담 {E(C['phone'])}</a><a class="btn btn-o" href="sms:{TEL}">문자로 사진 보내기</a></div>
</div></section>
<section class="sec"><div class="wrap post"><div class="post-body g-body">
  <h2>{E(n_kw)} {E(sym['name'])}, 현장에서 자주 보는 경우</h2>
  <p>{E(sym_text(TYPE_NOTE[ty][sym['slug']], n_kw))}</p>
  <p>{E(intro)}</p>
  {f'<h2>{E(n_kw)}에서 실제로 있었던 일</h2>' + case_story_html(posts, n_kw, sym) if (posts and is_local) else ''}
  {'' if is_local else area_list_html(base_slug, n_kw, sym)}
  <h2>{E(sym['name'])} 원인과 해결 방법</h2>
  {causes}
  {DIAGRAMS[sym['diags'][0]]() if sym['diags'] else ''}
  <h2>부르시기 전에 집에서 확인해 볼 것</h2>
  <ol class="g-list">{selfc}</ol>
  {'' if is_local else f'<div class="g-warn"><h3>이것만은 하지 마세요</h3><ul>{dont}</ul></div>'}
  {guide_link}
  <div class="tags">{tags}</div>
</div></div></section>
{case_sec}
{faq_html(faqs, f"{n_kw} {sym['name']} 자주 묻는 질문")}
<section class="sec"><div class="wrap"><h2>{E(n_kw)} 다른 전기 증상</h2><div class="chips">{other_sym}</div>
<h2 style="margin-top:28px">근처 동네 {E(sym['name'])}</h2><div class="chips">{near_links}{f'<a class="chip" href="{svc["slug"]}.html">{E(svc["short"])}</a>' if svc else ""}</div></div></section>
{cta(f"{n_kw} {sym['name']}, 지금 바로 상담하세요")}
""" + footer()
        write(f"{slug}.html", page)
        SYMPTOM_PAGES.append((f"{slug}.html", "0.7"))

def near_pages(base_slug, sym):
    """같은 지역의 다른 동네 + 지역 전체 페이지 링크"""
    lp = next((x for x in LOCALS if x["slug"] == base_slug), None)
    if lp:
        rg = next(x for x in REGIONS if x["slug"] == lp["region"])
        out = [(symptom_page_slug(o["slug"], sym), o.get("kn", o["name"])) for o in LOCALS if o["region"] == lp["region"] and o is not lp]
        out.append((symptom_page_slug(rg["slug"], sym), rg.get("alias") or rg["name"]))
        return [o for o in out if sym_built(o[0][:-len(sym["slug"])-1])]
    rg = next(x for x in REGIONS if x["slug"] == base_slug)
    out = [(symptom_page_slug(o["slug"], sym), o.get("kn", o["name"])) for o in LOCALS if o["region"] == base_slug]
    out += [(symptom_page_slug(o["slug"], sym), o.get("alias") or o["name"]) for o in REGIONS if o is not rg]
    return [o for o in out if sym_built(o[0][:-len(sym["slug"])-1])]

def sym_built(base_slug):
    lp = next((x for x in LOCALS if x["slug"] == base_slug), None)
    if lp: return has_cases(lp=lp)
    return False  # 지역 단위 증상 페이지는 동네 페이지와 내용이 80% 겹쳐 만들지 않음

def region_symptom_links_html(rg):
    nk = rg.get("alias") or rg["name"]
    locs = [l for l in LOCALS if l["region"] == rg["slug"] and sym_built(l["slug"])]
    cards = ""
    for sym in SYMPTOMS:
        g = next((x for x in GUIDES if x["slug"] == sym["guide"]), None)
        sub = "".join(f'<a href="{symptom_page_slug(l["slug"], sym)}.html">{E(l["kn"])}</a>' for l in locs)
        cards += (f'<div class="sym-c"><b>{E(nk)} {E(sym["name"])}</b><small>{E(sym["kws"][1])} · {E(sym["kws"][2])}</small>'
                  + (f'<span class="sym-sub">{sub}</span>' if sub else "")
                  + (f'<a class="link" href="{g["slug"]}.html">원인·확인 방법 보기 →</a>' if g else "") + "</div>")
    return f'<section class="sec"><div class="wrap"><h2>{E(nk)} 증상별 안내</h2><p class="sub">증상별 원인과 집에서 확인할 것, 동네별 실제 사례를 볼 수 있습니다.</p><div class="sym-grid">{cards}</div></div></section>'

def symptom_links_html(base_slug, n_kw):
    if not sym_built(base_slug): return ""
    li = "".join(f'<a class="sym-c" href="{symptom_page_slug(base_slug, s)}.html"><b>{E(n_kw)} {E(s["name"])}</b><small>{E(s["kws"][1])} · {E(s["kws"][2])}</small></a>' for s in SYMPTOMS)
    return f'<section class="sec"><div class="wrap"><h2>{E(n_kw)} 증상별 안내</h2><p class="sub">증상을 누르면 원인, 집에서 확인할 것, 실제 사례를 볼 수 있습니다.</p><div class="sym-grid">{li}</div></div></section>'

def has_cases(lp=None, rg=None):
    if lp: return any(any(m in (x.get("location") or "") + x["title"] for m in lp["match"]) for x in POSTS)
    return any(x["region"] == rg["name"] for x in POSTS)

def build_all_symptom_pages():
    for lp in [l for l in LOCALS if has_cases(lp=l)]:
        rg = next(x for x in REGIONS if x["slug"] == lp["region"])
        build_symptom_page(lp["slug"], lp["kn"], lp["full"], [(f"{rg['name']} 전기수리", f"{rg['slug']}.html"), (f"{lp['name']} 전기수리", f"{lp['slug']}.html")],
                           rg["name"], lp["near"], lp["intro"], scope_match=lp["match"])
    pass
