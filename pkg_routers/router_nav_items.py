import inspect
import json

from fastapi import APIRouter, HTTPException

from pkg_park4139_for_linux import DebuggingUtil, FastapiUtil, StateManagementUtil

router = APIRouter()



@router.put("/nav-items/reset")
def reset_nav_items():
    # FileSystemUtil.explorer(fr"{settings.protocol_type[0]}://{settings.host[0]}:{settings.port[0]}/make-dummy")
    NAV_ITEMS_JSON = StateManagementUtil.NAV_ITEMS_JSON
    dummy_cnt = 100
    dummy_data = [
        {
            "index": "141019e62de649698ec8d4d3ba9c065a20240205130022230734w",
            "title": "Vercel Hobby```",
            "href": "/Vercel Hobby```",
            "description": "\n# Vercel ?\nnetlify 와 사용 유사. 정적 웹을 배포하는데 이용할 수 있다.\nNext.js 개발팀에서 만든 호스팅 사이트, Next.js\nCI/CD 중 CD 설정 기능, 도메인 설정 기능, 웹 성능 모니터링 기능을 제공한다\n git hub/Vercel과 연동\ngit hub 에 push 하면, Vercel 에서 CD 수행\n\n# Vercel 도메인 설정\nVercel 에서 도메인을 직접 구매할 수 도 있고, 기존 도메인을 사용할 수 있다.\n도메인 설정을 하면 1년에 12달러라는 금액이 청구된다고 하는데\n나의 경우, 가비아에서 구매한 기존 도메인을 설정하였다.\n이것도 청구가 될런지 공식사이트의 내용을 찾아봐도 모르겠는데\n청구되면 2025년 2월 초에 청구될 수 있을 것 같다.\n\n# Vercel 기존 도메인 설정\nSettings > Domain > ~ > add\n\n# Vercel 가격 정책 설정\nhobby : 제약에 의한 무료 정책, 내가 현재 프로젝트에 적용한 정책 이다.\npro : 유료\nenterprise : 유료\n커스텀도메인 비용은 1년에 $12 만큼 따로 청구가 되지만 매년마다 한 번씩만 내면 되는 만큼 비용부담이 크진 않은 것 같다.\n비상업용 프로젝트를 배포한다면 100GB까지 무료,\n\n# Vercel 의 CI/CD 중 CD 지원\nVercel과 Github repository 연동을 해서 Github push 수행 시 Vercel은 Node.js 기반 프로젝트의 경우 Build 후 deploy 를 수행해준다.\n\n# Vercel에 배포시 환경변수 관리\nVercel에서 배포한 프로젝트의 settings를 클릭하면 Environment Variables메뉴가 있다. 거기서 key, value 라고 하는게\n환경변수를 의미한다. 원하는 설정해주고 재배포하면 적용이 되는것을 확인할 수 있다.\n특히, Next.js 프로젝트 배포 시 환경변수는 .env.local 파일과 연동이 되는데. Vercel 의 환경변수에 설정을 하도록 디자인 되어있다. .env.local 파일은 .gitignore 에 자동 추가된다. 이는 op가 아닌 dev 에서만 적용되도록 디자인 됨을 의미.이 점을 이용하면 local 에서 dev에서 사용되는 변수와 op에서 사용되는 변수를\n차등을 두어 설정 할 수 있다. 예를 들면 .env.local 에는 NEXT_PUBLIC_NAVITEMS_API_ADDRESS = {로컬용 변수값}  이런식으로 써두고 \nVercel 에서는 NEXT_PUBLIC_NAVITEMS_API_ADDRESS = {원격용 변수값} 이런 식으로 작성하면 배포 시에는 {원격용 변수값} 으로 overwrite 되어진 것 처럼 적용된다.\n\n# Vercel 무료 라인으로 Next.js 배포 했는데 페이지 렌더링이 안되는 경우\nVercel 대시보드에서 \"settings\" 탭으로 이동하여 \"data cache \" 옵션을 클릭하고 purge everything\n이를 통해서 캐싱된 데이터를 지운다\n\n# Vercel을 통해 나의 배포 중인 프로젝트들 확인\nhttps://Vercel.com/jung-hoon-parks-projects\n\n# Vercel redeploy 평균시간 측정(5회 사이클 테스트 결과)\n현재 프로젝트 기준 평균적으로 54sec 초 정도 operation freeze 되는 것이 측정되었다.\n\n# Vercel 캐시 삭제 안됨(테스트 필요)\n프로젝트와 연동된 창을 닫고 혹시 몰라 ctrl f5 를 누르고 Vercel/settings/purge 하고 redeploy\n"
        },
        {
            "index": "24d2d50665bc4dab9f36b6535d272fd020240205213554605663W",
            "title": "Node.js 21.4.0```",
            "href": "/Node.js 21.4.0```",
            "description": "\n# Node.js\n\"js 해석엔진\" \"웹브라우져 안\"에 내장되어 있으며 \"웹을 위해 작성된 js 코드\"를 동작시킨다\n구체적 예시로는 chrome v8, firefox spiderMonkey 등 이 있다\n여기서, chrome v8 을 web 뿐 아니라 다른 application 에서도 코드를 동작시킬 수 있도록 \"chrome 웹브라우져\" 에서 분리해서 출시하였다.\n그게 Node.js 이다, Node.js 가 컴퓨터에 설치 되어 있으면, 그 컴퓨터는 javascript 코드를 동작시킬 수 있다.\n다른말로, 그 컴퓨터는 javascript 실행환경을 준비했다고 할 수 있음.\n\n# Node.js non-blocking I/O 특성\nNode.js는 non-blocking I/O 특성으로, 상대적으로 더 많은 easy 요청을 처리할 수 있다.\nhard work 1, easy work 1, easy work 2, easy work 3 이게 무작위로 요청들어오면\neasy work 부터 처리하고 나중에 hard work 처리한다. 이 동작방식은 hard work 처리하느라 easy work 가 delay 되는 것을 방지.\n따라서, 상대적으로 더 많은 easy 요청을 처리할 수 있다. 이 특성을 이용하면 요청이 많은 곳은 Node.js 를 쓰는게 유리하다\n이것이 잦고 빈번한 낮은 CPU 리소스 요구 수준의 요청을 처리하는 웹서버에 Node.js 가 적합한 이유이다.\n조금더 구체적으로는 요청이 많은 곳의 예시는 SNS, 채팅서비스 이다.\n\n#Node.js npm\nNode.js 내의 js 라이브러리 관리(설치수정삭제) 용이\n\n#Node.js npm run\nNode.js 프로젝트에서 package.json 파일에 정의된 스크립트를 실행하는 데 사용됩니다.\n\n#Node.js npm run dev\n개발 서버에서 실행할때 사용\n\n#Node.js npm run build\n빌드 테스트 진행 시 사용\n\n#Node.js package.json\n프로젝트의 의존성 관리 및 스크립트 실행에 사용되는 정보를 포함하는 파일입니다.\n\n# Node.js 서버스케일링/서버멀티쓰레딩 을 통해서 영화예매접수창구 를 늘리듯 가능.\n단일 스레드로 동작하기 때문에 CPU 집약적인 작업이 많은 애플리케이션에는 적합하지 않을 수 있습니다.\n장기 실행되는 작업이 많은 경우 이벤트 루프를 막을 수 있어야 한다고 한다.\n서버 부하가 많은 상황에서는 성능이 저하될 수 있습니다.\nJava는 대규모 애플리케이션과 엔터프라이즈 솔루션에 적합하며,\n\n# Node.js 적합한 예시(모범사례)\nNode.js는 가벼운 애플리케이션과 실시간 웹 애플리케이션에 적합\n\n#Node.js index.js 에 mysql 직접 연결 (without DB api)\n index.js은 js로 작성되어 있으며, Node.js 과 같은 js 해석기에 의존\nnpm install nodemon\nnpm install mysql\nnpm uninstall mysql\nnpm update mysql\nnpm run build\nindex.js\n    import * as from 'mysql'\n    console.log(\"hello javascript\")\nnode index.js\n nodemon index.js\n\n"
        },
        {
            "index": "2ab34943e56948aebafd0c18ddf0dfa320240206013919102693C",
            "title": "React.js 18.2.0```",
            "href": "/React.js 18.2.0```",
            "description": "\n# React\nUI 개발용 자바스크립트 라이브러리\nmeta 가 facebook 시절 개발\n재사용 가능한 사용자 인터페이스(UI) 컴포넌트를 구축하는데 중점을 둡니다.\n가상 DOM과 컴포넌트 기반 아키텍처를 특징으로 합니다. 이를 통해 개발자는 웹 애플리케이션의 성능을 향상시키고 유지보수를 용이하게 할 수 있습니다.\n\n# React 가상 DOM(Virtual DOM)\n가상 DOM은 웹 페이지의 실제 DOM(Document Object Model)과 대응되는 가벼운 복사본이며,\nReact는 이를 사용하여 효율적인 업데이트를 가능하게 합니다. 상태(state)와 속성(props)의 변화를 감지하고,\n필요한 부분만 실제 DOM에 반영하여 UI를 업데이트합니다. 이는 성능을 향상시키고 웹 애플리케이션의 반응성을 높여줍니다.\n\n# React 컴포넌트\n컴포넌트 기반 flutter 가 wiget 기반 architecture 를 사용하는 것과 유사하다.\n컴포넌트 기반 아키텍처를 채택하여 UI를 작은 단위로 나누고 관리.\n각 컴포넌트는 재사용 가능하고 유지보수가 용이합니다. 독립적으로 작동하며.\n\n# React JSX\n자바스크립트 코드 안에 HTML과 유사구문을 작성할 수 있게 해줍니다.\n\n# React SPA\nSingle Page Application(단일 페이지 애플리케이션)과 함께 사용되는 것이 일반적이지만,\n다른 프레임워크나 라이브러리와도 조합하여 사용할 수 있습니다.\n또한 React 네이티브(React Native)를 사용하면 웹이 아닌 모바일 애플리케이션도 개발할 수 있습니다.\n\n\n"
        },
        {
            "index": "df15ed45bd2d41d3a535910a1f099fa120240202005842783061g",
            "title": "Next.js 14.0.4```",
            "href": "/Next.js 14.0.4```",
            "description": "\n# Next.js CSR 과 Client Side 라우팅\n독특하다. create\\[id] 라니. 실제 구현된 프로젝트에서는 페이지별로 관리하게 되는 패턴이 여럿 보았는데.\n이 부분을 경로로서 create\\[id] 로 직관적으로 구현해낸 것 같다. 이 프로젝트에서는\ncreate/[id] 를 페이지 요청을 할때 create\\[id] 로 들어가서 확인하면 된다.\n페이지명 작명도 필요없다. page.js 로 통일할 수 있다.\n\n# Next.js SSR\nNext.js 는 과거의 서버사이드랜더링 과 CSR 의 각 장점들을 포커싱하여 하이브리드 로서 설계한 것 같다.\nSSR은 이는 사용자의 리소스 사용을 줄이고 서버에서 일을 해주겠다! 서버가 좋아야 겠지\n덧붙여, react.js 는 CSR 기반으로 동작하는 것으로 알고 있으며, Next.js 는 CSR/SSR 모두 지원할 수 있다.\n\n# Next.js SPA\nweb app 을 구현하는 양상 중에 SPA 란 개념으로 구성된 것 같다. 마치 mobile 의 app 처럼 동작한다.\n한페이지에서 말이다. 아주 아주 페이지의 변화가 부드러운 것이 특징이다.\n덧붙여, 이는 소비자의 결제가능성과 매우 직결되는 요소라고 한다.\n\n# Next.js compile 에러 헌팅\nfoo.tsx 를 꼭써야 compile 에러를 가이드해준다\nfoo.ts 와 foo.tsx 의 차이는\n\n# Next.js 의 CSR component vs SSR component\nNext.js 는 컴포넌트 기반의 컨셉으로 만들어진다. flutter 의 wiget 개념과 유사하다.\n특히 컴포넌트는 두개의 서로 다른 특성의 컴포넌트를 구현되는데.\n이 두개가 CSR component, SSR component 이다.\nNext.js 기본베이스는 SSR component 으로 설정된다 생각을 하면 되는 것 같다.\n원하는데로 SSR 을 지향하는 기능/CSR로 기능을 선택 구현할 수 있다.\n각 기능에 따라 Rendering 에 대한 지향이 다르다고 한다.\n예를 들어 client 의 click 의해 동작해야 하는 경우, \"use client\"; 를 써가며 CSR로 기능을 구현한다.\n\n# Next.js Type error: Parameter 'props' implicitly has an 'any' type.\nnpm install --save-dev @types/react @types/react-dom\nTry restarting your IDE and development server.\n\n# Next.js 리디렉션 via CSR\n// router.push(`/read/${result.id}`) // 리디렉션시킴 Client side 기능\n// router.push(`/home`); // 리디렉션시킴 Client side 기능\n\n# Next.js 상태관리 대안(클라이언트 측에서 정보를 유지하는 대안들)\n1. React Context API: React의 Context API는 상위 컴포넌트에서 하위 컴포넌트로 데이터를 전달하는 메커니즘을 제공합니다. 클라이언트 측에서 클릭된 버튼의 정보를 Context로 관리하여 해당 정보를 필요로 하는 컴포넌트에서 접근하고 업데이트할 수 있습니다.\n2. Next.js의 내장 상태 관리 기능:\n    Next.js는 페이지 간에 상태를 유지하기 위한 내장 상태 관리 기능을 제공합니다. getServerSideProps 또는 getStaticProps를 사용하여 서버 측에서 상태를 가져와 초기 상태로 설정하고,\n    클라이언트 측에서는 상태를 유지하여 업데이트할 수 있습니다.\n3. React 상태 관리 라이브러리 (예: Redux, MobX, recoil): Redux나 MobX와 같은 상태 관리 라이브러리를 사용하여 클라이언트 측에서 클릭된 버튼의 정보를 상태로 관리할 수 있습니다. 이를 통해 상태를 중앙 집중식으로 관리하고, 다른 컴포넌트에서도 해당 상태에 접근하여 업데이트할 수 있습니다.\n4. 로컬 스토리지 (Local Storage) 또는 세션 스토리지 (Session Storage):\n    클라이언트 측에서 클릭된 버튼의 정보를 로컬 스토리지나 세션 스토리지에 저장할 수 있습니다.\n    이를 통해 페이지를 새로고침하거나 이동해도 정보를 유지할 수 있습니다.\nCookie 나 Sessions 는 object 를 저장 못하고. string 만 저장 가능하다.\n\n# Next.js 상태관리 라이브러리\nNext.js 상태관리 라이브러리 는 mobile 처럼 상태관리 라이브러리가 매우 인기있다.\nrecoil/redux/zustand/React Query 등등\n\n# Next.js React-query\n이름에 쿼리가 붙길래 DB api 라이브러리 같은 건줄 알았다.\nredux/recoil 등의 상태관리 라이브러리 의 boilerplate 를 어느정도 해소해준다\n비동기 통신 후 data formatting 을 하며 발생되는 비효율을 자동화된 caching을 통해 줄여주는 라이블러리로 보인다.\n\n# Next.js 웹타이틀 설정\n    client side component\n        export const metadata ={\n          title:\"readAll\",\n          description:\"readAll\",\n        }\n    server side component\n        export const metadata ={\n          title:\"readAll\",\n          description:\"readAll\",\n        }\n\n\n# Next.js 프로젝트만을 위한 reindentation + 에러 색인 설정\n설정을 적용하면 코드가 Prettier에 의해 자동으로 정렬되고 파일을 저장할 때마다 ESLint에 의해 오류가 확인\nnpm install prettier --save-dev\nnpm install eslint --save-dev\nnpm install eslint-config-prettier --save-dev\n루트 프로젝트에 .eslintrc.json 파일 생성 후 아래내용을 추가\n    {\n      \"extends\": [\"next\", \"next/core-web-vitals\", \"prettier\"],\n      \"plugins\": [],\n      \"rules\": {}\n    }\n    유의사항, Prettier는 수정 후 형식이 적용되도록 이 배열의 마지막에 배치.\n        vscode 의 settings.json 에 아래내용을 추가\n            {\n              \"editor.defaultFormatter\": \"esbenp.prettier-vscode\",\n              \"editor.formatOnSave\": true,\n              \"editor.codeActionsOnSave\": {\n                \"source.fixAll.eslint\": true\n              }\n            }\n\n# Next.js 에러페이지 못 찾는 문제\nError: Could not find the module \"C:\blah\blah\\link.js#\" in the React Client Manifest. This is probably a bug in the React Server Components bundler.\n진짜 문제였음.\n해당 에러는 React Server Components 번들러에서 발생하는 버그로 인해 \"C:\\projects\\services\\e_magazine\node_modules\next\\dist\\client\\link.js\n이러한 경우 다음과 같은 조치를 취할 수 있습니다:\nnpm install 만 명령어로 써서 update 하니 해결됨.\n\n# Next.js 프로젝트에 recoil 적용\nnpm i recoil\n\"use client\";\nlayout.tsx에서 import { RecoilRoot } from 'recoil';\nlayout.tsx에서 최상단을 감싸줌 <RecoilRoot></RecoilRoot>\natom제작\n\n# recoil 에서 가져오기\nuseSetRecoilState/useRecoilValue 는 react Hook이기 때문에 useEffect의 안에서 사용할 수 없다.\nconst [navItemsAtom, setNavItemsAtom] = useRecoilState(NavItemsAtom);  // 이 코드는 single page 에서만 state 가 유지되는 방법으로 의도한 여러 pages 에서는 state 를 유지할 수 없음.\nconst value = useRecoilValue(아톰)\nconst setValue = useSetRecoilState(아톰)\n\n# redux 에 저장 vs recoil 에 저장\nrecoil 은 컴포넌트 간에 상태를 공유, object 형태 저장 가능!\nRedux는 전역 상태 관리 라이브러리로, 여러 페이지 간에 상태를 공유하고 유지\nrecoil은 한 페이지 내에서 상태를 관리하고 공유하는 데에 적합하며, Redux는 여러 페이지 간에 상태를 관리하고 공유하는 데에 적합\n한페이지에서 recoil 로 저장해두고 다른페이지에서 recoil 내의 값을 가져올 수 없는 이유\n\n# cookie 에 저장\ncookie:\n쿠키는 일반적으로 문자열 형태로 데이터를 저장하고 전송하는 용도로 사용, json 형태로는 저장 불가, 특정 문자 제한이 있으므로, 필요에 따라 문자열을 인코딩하여 저장해야 할 수도 있다.\n웹 브라우저에는 정보를 저장하고 cookie id 만 서버에서 조회를 하는 way ,\n세션에 대해서 상대적으로 client request 가 많아질 수록 network traffic 에 부하를 줄일 수 있는 방법(인증, 개인화, 방문자의 상태 체크)를 방법 , 쿠키는 서버 트래픽에 대해 친화적\n\n# session 에 저장\nsession: 웹 서버에만 정보를 남기면서 cookie 에 비해서 상대적으로 안전하게를 방법 , 세션은 사용자 데이터 보안에 대해 친화적\n\n# redux 에 저장\nredux 는 페이지들 전역으로 공유 object 를 쓸 수 있단다. redux 또한 client side 상태관리용 storage 로 생각하면 되겠다.\nredux 는 javascript 의존한다. react, Next.js 가 아니라. cdn 으로도 지원하나봄.\nnpm install redux react-redux \n최근에는 Redux Toolkit과 같은 Redux의 공식적인 도구들이 도입되면서, 보다 간편하고 편리한 Redux 사용 방법이 제공되고 있습니다.\nRedux Toolkit은 Redux 애플리케이션을 더 쉽게 작성하고 관리할 수 있는 공식적인 도구 세트입니다. Redux Toolkit을 사용하면 Redux의 설정과 보일러플레이트 코드를 줄일 수 있으며, 간편한 문법과 유틸리티 함수들을 제공하여 개발 생산성을 향상시킵니다.\nRedux Toolkit을 사용하여 Redux를 설정하는 방법은 다음과 같습니다:\nRedux Toolkit 설치: 프로젝트 디렉토리에서 Redux Toolkit을 설치합니다. 다음 명령어를 사용할 수 있습니다:\nnpm install @reduxjs/toolkit\nnpm uninstall @reduxjs/toolkit\n\n# zustand 에 저장\nnpm install zustand\nconst useZustandStore = create((set)=>({\n    count : 0,\n    addCountOne(){\n      set((state:any)=>({count: state.count +1}))\n    },\n}))\nconst useZustandStore2 = create((set)=>({// store 여러개 만들 수 있음 !\n    async ajaxRequest(){// 이런 것도 된다고 한다 무려 비동기 함수를 말이야. 모든페이지의 전역으로 저장. ㅎㄷㄷ\n        const response  = await fetch(\"https://~~~\");\n        console.log(await response.json());\n    }\n}))\n# zustand 에서 가져오기\nconst {count, addCountOne} = useZustandStore();\nalert(count)\naddCountOne()\nimport {devtools} from 'zustand/middleware'\n\n# localStorage 에 저장\nlocalStorage의 브라우저에 있는 저장소, 용량은 브라우저마다 다름. 일반적으로 5MB에서 10MB 사이의 용량, 사용자의 장치 설정에 따라 변경될 수도 있습니다.\nlocalStorage는 클라이언트 사이드에서 사용하는 저장소입니다. 데이터는 브라우저의 로컬 스토리지에 저장되며, 서버와의 통신 없이 클라이언트에서 직접 접근할 수 있습니다. 이를 통해 웹 애플리케이션은 사용자의 로컬 환경에서 데이터를 유지하고 관리할 수 있습니다.\nlocalStorage에 데이터를 저장하고 가져오는 방법은 이전 예시에서 설명한 것과 같습니다. localStorage.setItem() 메서드로 데이터를 저장하고, localStorage.getItem() 메서드로 데이터를 가져올 수 있습니다. 데이터는 문자열 형태로 저장되므로, 객체를 문자열로 변환하여 저장하고, 가져올 때는 문자열을 다시 객체로 변환해야 합니다.\nconst userString = JSON.stringify(user);\nlocalStorage.setItem('user', userString);\nlocalStorage 에서 가져오기\nconst storedUserString = localStorage.getItem('user');\nconst storedUser = JSON.parse(storedUserString);\nconsole.log(storedUser.name); // 출력: John\nconsole.log(storedUser.age); // 출력: 25\n\n# Next.js 프로젝트에서 데이터를 object 형태로 저장할 수 있는건\nrecoil/redux\n대부분 string 형태로 저장만 가능,\n\n# Next.js 프로젝트 vscode 에서 자동 import 안되는 현상\n자동 import 하려고 애를 써도 안된다. extension 설치 여러개 해도 안댄다.\n.js 로 atom 을 만들어서 그렇다. .tsx 로 만들어야 파일을 확인하나 봄.\n이제 댄다.\n\n# zustand 설정 때문에  build 가 안되는 현상.\n:any || {}:any  || (:any)타입캐스팅을 해주자\n\n# create 페이지는 client component 로 만드는게 일반적이다.\nNext.js 에서는 client component 로 async 키워드를 사용못하도록 제한한다.\n만약 client component 이면서 server component 기능을 둘 다 쓰고 싶으면 , \"use client\"; 키워드를 사용해야한다. 최적화 고민이 추후에 필요한 부분이라는 것 같다.\n그러나 이 페이지의 기획에서는 지금 두개 구현이 한페이지에 다필요하다. 그래서 경고가 뜨는 것 같다.\n이 페이지에서는 nav 는 비동기로 json 서버쪽에서 데이터 받아와서 목록을 만들어야하고, create 하는 부분은 client component 를 이용해야 한다.\n새로 알게된 사실인데,이 경우는 따로 파일을 만들어 해결할 수 있다. client side 로 처리할 부분만 vscode 의 전구의 누르고 move to a new file 을 눌러 CS 부분만 빠르게 추출해서 파일을 만들 수 있다.\n이제 경고 없이 한페이지에서 CS 기능과 SS 기능을 구현할 수 있다.\n\n# 타입캐스팅\n가능하면 타입을 바꿔줌\n(e.target.title as HTMLTextereaElement).value\njs 에서 타입캐스팅\n\n# 타입힌팅\n타입을 명시적으로 가이드해줌\n:string\npython 에서 parameter/변수에\n"
        },
        {
            "index": "2fd60a92619f4cd9a898d79c99b1715720240206031133837128y",
            "title": "AWS EC2 t2.micro```",
            "href": "/AWS EC2 t2.micro```",
            "description": "\n# AWS EC2 instance\nAWS EC2(Amazon Elastic Compute Cloud)는 클라우드에서 가상 서버를 제공하는 서비스입니다.\nEC2 인스턴스는 다양한 운영 체제와 소프트웨어 구성을 지원하며, 필요에 따라 유연하게 스케일링할 수 있습니다.\nEC2 인스턴스는 컴퓨팅 리소스를 필요한 만큼만 사용하므로 비용 효율적이며, 범용, 컴퓨팅 최적화, 메모리 최적화, 스토리지 최적화 등 다양한 인스턴스 유형을 제공합니다. \n또한 EC2는 다양한 네트워킹 및 보안 기능을 제공하여 안전하고 신뢰할 수 있는 환경을 구축할 수 있습니다. \nEC2 인스턴스는 개발, 테스트, 웹 애플리케이션 호스팅, 데이터베이스 관리 등 다양한 용도로 사용됩니다.\n인스턴스명 t2.micro 를 무료로 빌렸다.\n\n# AWS EC2 무료사용 기준\nAWS Free Tier 서비스\n1년 무료, 반드시 컴퓨터 1대 만 무료\n고정 IP 로 설정 하지 않으면 과금(탄력적 IP 설정 필수)\n정해진 기준을 넘어서면 과금한다.\n클라우드 컴퓨팅을 통한 서비스 프로덕션 배포.\naws key 를 public 으로 올리면 절대 안된다. 해커에 의한 과금 수천만원 빚더미를 안을 수 있다?\naws 계정을 1년 이내에 계정 해제(인스턴스 삭제?)를 해야한다.(인스턴스 시작일이 2024 01 25 이니 넉넉잡아 2024 12 월에 계정해제 를 해야겠다)\n참고로 인스턴스 종료 시 삭제 설정이 경험적으로 default 였고, 인스턴스 삭제를 원하면 인스턴스 종료를 하면 된다.\n\n# aws ec2 instance 머신 방화벽 설정\naws ec2 네스워크 설정  \n네트워크 및 보안  \nssh 유형의 보안그룹만 선택\n인바운드 규칙 편집\n규칙 추가\nCIDR 블록 적당히 설정 // CIDR 은  IP주소 할당 방법, 0.0.0.0/0 으로 22/80/443 설정 안하면 certbot 못쓸 수 있음.\nsecurity-group-for-fastapi // 보안 그룹 이름\n\"포트 범위\" 에 포트 번호(귀하의 경우 8080 )를 입력한 다음 \"규칙 추가\"를 클릭하세요.\n드롭다운을 사용하여 HTTP( 포트 80 ) 를 추가합니다.\n\n# 도메인 과 aws ec2 연결(무료 도메인), fail, 무료 도메인 제공업체인 freenom 에러로 진행불가, 값싼 도메인으로 대체진행\nfreenom\n제한에 따른 무료 도메인 제공\nTLD 제약큼.\n연장 시기 놓치면 유료화 서비스로 전환\n기준 이상 트래픽 발생 시 유료화 서비스로 전환(ment 에 special domain 관련 이야기 나오면 유의)\n도메인 재발급에 의한 기존사용자 서비스 신뢰성 훼손\n도메인 소유권을 freenom 에서 강제로 가져갈 수 있음. https://namu.wiki/w/Freenom\n구글 로그인\n구글 혹은 페이스북 로그인시 your social login could not be determined 에러.\nFreenom 회원가입, 도메인을 등록하지 않은 상태에서는 회원가입 진행불가\n위의 안내에 따라 도메인을 선택해서 등록진행하다보면 회원가입할 수 있다.\n도메인이 등록된 이후에는 정상적으로 로그인이 가능하다.\nservices/register a new domain\nFreenom 중요 공지: 기술적인 문제로 인해 신규 등록을 위한 Freenom 신청이 일시적으로 중단되었습니다.\n불편을 끼쳐드려 죄송합니다. 우리는 해결책을 찾기 위해 노력하고 있으며 곧 운영을 재개할 수 있기를 바랍니다.\n이해해 주셔서 감사합니다...라고 한다\nfreenom 설정 불가...대체 서비스 모색\nfreenom replacement service\nfreenom alternatives\n\n# 도메인 과 aws ec2 연결(값싼 도메인), success\n가비아(도메인 호스팅 유명 대형 업체)의 이벤트로 값싼 도메인 구매를 진행\n도메인 1개 1년간 500원, 500원 결제하려 해도 안됨, 최소결제 비용 1000원 제한을 이유로.\n그래서 2개 구매하였음 1100원 결제 // 500원 짜리 2개 구매, 부가세 10% 적용, 이유는 모르겠는데 결제 시도하는데 엄청 느렸음...\n구글로그인  \n안전 잠금 서비스 // 2024 01 31 기준으로 무료확인. 개발 및 토이프로젝트는 설정말고/프로덕션이면 설정하자\n가비아 네임서버 사용// 네임서버 설정\n도메인 구매 후 적용되는 데 걸리는 시간, 루트서버 갱신 및 네임서버 캐시에 따라, 적용되는데 1~2일 정도 소요될 수 있습니다.\n\n# aws Route53 서비스 NS/SOA 레코드 설정\naws DNS 라우팅 서비스\nDomain 과 AWS의 EC2 인스턴스 연결\n레코드 생성\n\n"
        },
        {
            "index": "e61332b60de84ad5a3e74284123d7a9920240206034532690231s",
            "title": "Ubuntu 22.04```",
            "href": "/Ubuntu 22.04```",
            "description": "\n# Ubuntu?\nlimited free license OS\nopensource OS\n\n#리눅스 \n다중 작업과 다중 사용자, 다중 스레드를 지원하는 일반적인 OS 입니다\n개발자의 커스터마이징이 자유로운 OS\nC언어 에 의해서 많은 개발이 되었음 C언어를 잘하는 개발자라면 리눅스  를 사용하면서 어지간한 리눅스  의 구성요소들을 직접 들여다보고 수정하고 개발 할 수 있는 장점이 있습니다.\n리눅스  는 다른 OS 들과는 상대적으로 하드웨어의 사양이 그렇게 높지 않아도 운영가능. 덧붙여,전 세계적으로도 어려운 사람이나 국가에 PC를 보급 할때보면 OS 는 리눅스  로 보급을 하고 있습니다.\n전 세계에 보급된 스마트 폰의 7~80% 이상은 리눅스  커널을 사용하는 안드로이드\n복잡하게 여러군데를 뒤지지 않고 커멘드로 복잡한 작업을 한번에 해치울수도 있습니다.\n\n#리눅스  장점\n리눅스  는 하나의 PC에 여러명이 접속 하여 여러개의 program 을 동시에 실행하거나 작업 할 수 있는 장점이 있습니다\n\n#리눅스 kernel\nOS 의 핵심이 되는 program\n\n#리눅스 shell\n커널에 명령을 전달하는 program .\n사용자와 OS  사이를 Interface시키는 하나의 유틸리티 program 이며\n사용자로부터 받은 명령을 kernel이 이해하도록 해석하여 전달하는 명령어 해석기\n쉘은 사용자가 입력한 명령 라인을 읽어들여 해석하고 리눅스   시스템을 통해서 명령 라인이 실행되게 하는 Command Interpreter(명령을 한줄씩 해석)\n쉘도 여러가지 종류가 있으며,\n리눅스  의 경우 /etc/shells 을 열어서 확인 가능\n/bin/sh\n    최초로 만들어진 표준 쉘로 복구 모드에 사용된다.\n    우분투에서 /bin/sh는 dash로 링크가 걸려있다.\n/bin/bash\n    리눅스  에서 가장 대표적으로 사용되는 쉘이다.\n    기능이 많은 대신 dash보다 다소 느리다고 한다.\nshell programing\n\n#리눅스 foo.sh\n쉘스크립트\n반복 실행\n스케쥴링\n\n# 리눅스 콘솔 청소\nclear\n\n# 리눅스 terminal 제어\nalt + D : 현재 커서 위치에서 그 단어 끝부분까지 텍스트 지우기\nalt + Backspace : 현재 커서 위치에서 그 단어 앞부분까지 텍스트 지우기 \n\n# 리눅스 신규 계정 생성\nubuntu config --default-user root\nwsl\nsudo useradd 사용자계정\nsudo passwd 사용자계정\n패스워드\ncat /etc/passwd | grep 사용자계정\n\n# 리눅스 계정 sudo 권한 추가(+NOPASSWD)\necho '사용자계정 ALL=NOPASSWD: ALL' >> /etc/sudoers\ncat /etc/sudoers | tail -2\n\n# 리눅스 패스워드 입력 없이 sudo 명령어 사용 설정\nsu - 사용자계정\nsudo reboot\nubuntu config --default-user 사용자계정\nwsl\nsudo reboot\n\n#리눅스 명령어로 클립보드로 저장하는 방법 # ctrl c 하지 않고 클립보드로 저장하는 방법\nsudo apt-get install -y xclip\npwd | xclip -sel clip\necho \"test\" | xclip -sel clip\n\n# 리눅스 변수 제어\nARRAY=(행복해 정말행복해 행복해 정말행복해)\necho ${ARRAY[*]}\nvar1=사랑해\nvar2=재밌어\nvar3=고마워\nvar4=행복해\necho ${var4}\necho ${var5:=변수초기화되지않았다면이것으로바뀝니다}\necho $0\necho $1\necho $2\necho $3\necho $4\necho $5\necho $6\necho $7\necho $8\necho $9\necho 전달된 인수의 수는 $# 개 입니다.\necho 모든인수를 $* 로 한번에 처리할 수 있습니다.\necho 직전 커멘드의 실행결과 는 $? 입니다.0=success\necho 해당 shell script의 PID 는 $$ 입니다.\necho 마지막으로 실행한 shell script PID 는 $! 입니다.\nexplainShell () {\n    echo \"쉘 스크립트에서는 function 를 쓸 수 있습니다\"\n}\nexplainShell\n\n\n\n#리눅스 directory 제어\nmkdir foo\nrmdir foo\nrm -r foo\ncp tmp tmp2\n\n#리눅스 file 제어\ntouch foo.txt // make file\ncat foo.txt // open file\nrm foo.txt\ntouch tmp.sh\n~/Desktop/tmp.sh // run tmp.sh\n./tmp.sh         // run tmp.sh\ncd ~/tmp.sh      // run tmp.sh\n\n#리눅스 pip 설치\nsudo apt-get update\nsudo apt-get install python3-pip\n\n#리눅스 모든 파이썬 package 삭제\npip freeze > uninstall.txt\nchmod 777 uninstall.txt\npip uninstall -r uninstall.txt\npip list\n삭제 uninstall.txt\n\n"
        },
        {
            "index": "8c747132ff064a4682ac9d1f1c88022120240206034649718424C",
            "title": "Nginx 1.18.0```",
            "href": "/Nginx 1.18.0```",
            "description": "\n# nginx?\nweb server/load balancer/proxy server 역할 가능.\nproxy 설정 가능(nginx에서 80포트에 request가 들어오면 8000번 포트(uvicorn default port)에 포워딩)\n\n# nginx dependency 설치\ninstall dependencies for fastapi service and run service\nsudo apt-get update\nsudo apt update\nsudo apt install -y nginx\n\n# nginx 설정  with proxy 설정 + with CORS *로 설정 + with 도메인 + with TLS\n어떤 파일을 수정해야 하는지 결정하기 위해서는 변경하려는 설정의 범위를 고려해야 합니다.\n전체 nginx 서버에 영향을 주는 설정이라면 /etc/nginx/nginx.conf를 수정하면 되고,\n특정 사이트에 대한 설정이라면 /etc/nginx/sites-enabled/ 디렉토리 내의 해당 사이트 파일을 수정하면 됩니다.\n\n# 무료 SSL/TLS 설정\ncertbot 이라는 리눅스  패키지 가 있다.\ncertbot 은 Let's Encrypt CA 를 통하여 무료 TLS 인증을 받을 수 있다. 이 무료 인증은 3개월 유효기간을 가지며, 이 인증은 무료로 갱신할 수 있다.\n이 또한 certbot을 통해서 쉽게 자동갱신을 설정할 수 있으며 crontab 리눅스  패키지를 통해서\n인증서 갱신 자동화를 스케쥴링 할 수 있다.\n덧붙여, public IP 으로 ssl 지원 미지원 한다. 유로로 서비스하는 업체도 드물지만 있다. 따라서, api를 구축 중이기 떄문에 도메인이 불필요 했던 나는, 도메인을 구매없이 진행하려던 것은 실패하였다. (https://000.0.0.0:8080 로는 SSL을 일반적으로 설정하지 않음)\ndomain 으로 ssl 지원 가능\n// aws ec2 instance 에서 ssl 설정, 이것도 무료라는 것 같다, 이것 보다는 nginx 에서 ssl 설정하는 것이 유지보수가 용이하여 인기가 있어 보이는 것 같다.\nnginx 에서 ssl 설정\n// uvicorn 에서 ssl 설정 // 일반적으로 uvicorn 에서 ssl 설정을 하지 않고, nginx 같은 프로그램에서 포워딩 되도록 설정하는 것 같아 보인다.\n// nginx TLS 공인인증 설정\n// TLS 공인인증서 생성 via certbot\n// 가비아 에서 domain 을 구매 후 aws EC2 instance 머신에 nginx와 certbot 인증서 직접적으로 설치 및 설정 진행\n// 덧붙여, 가비아 서비스를 이용 시에는, AWS DNS 서비스의 필터들을 지워주어야 해당 도메인이 검색된다고 합니다.\n// 덧붙여, AWS HTTPS 를 사용하기 위해서는 AWS DNS 서비스를 이용하여 도메인을 적용해야합니다.\ncertbot --version\nsudo apt-get update\nsudo snap install core\nsudo snap refresh core\n//sudo apt-get install software-properties-common\n//sudo add-apt-repository universe\n//sudo apt-get update\n//sudo apt-get install certbot -y\n//sudo apt-get install python3-certbot-nginx -y\nsudo apt-get remove certbot -y // certbot명령어를 사용할 때 snap이 사용되게 하기 위함 - certbot 공식가이드 -\nsudo snap install --classic certbot // certbot 재설치, certbot 공식문서에서는 snap 으로 설치할 것을 가이드, Ubuntu 가 16.04 LTS 이상인 경우,snap 은 built in packgage 이다.\nsudo ln -s /snap/bin/certbot /usr/bin/certbot\nwhich snap\nwhich certbot\nsudo certbot --nginx -d 도메인 \n\n# certbot error:  Timeout during connect (likely firewall problem)\nwget my.ip.address // fail 이면 aws 방화벽 설정이 포워딩을 막고 있을 수 있음.\naws console // 조사해보니 80 포트 인바운드 규칙 CIDR 블록이  0.0.0.0/0 아니고 특정 host와 port 대역으로 설정되어 있었음 0.0.0.0/0 로 저장\nsudo ufw status // 방화벽 확인 // inactive 되어 있어야 한다.\n\n# 인증서 갱신(수동)\nsudo certbot renew --dry-run // 인증서 갱신(수동) 테스트, --dry-run 명령을 실제로 실행하지 않고 결과 값을 알려주는 옵션\nsudo certbot renew // 인증서 갱신(수동), 인증서 유효기간 3개월인데 crontab 으로 자동화 설정 가능)\n\n# 인증서 갱신 자동화 설정 via crontab\nsudo crontab -e\n2 // crontab 옵션\n// 80일마다 새벽 2시에 certbot 을 통한 무료인증서 갱신 자동화\n0 2 */80 * * /usr/bin/certbot renew --quiet\n\n# nginx restart\nsudo service nginx restart\nsystemctl status nginx.service\n\n# 무료인증서 만료일자 확인\nsudo certbot certificates\n\n# SSL/TLS 적용완료 테스트\nexplorer https://도메인/docs\ncurl -X GET https://도메인/\ncurl -X GET https://도메인/nav-items\ncurl -X GET https://도메인/nav-items/0\ncurl -X GET https://도메인/nav-items/1\n\n"
        },
        {
            "index": "99f92cce88b3414c8a14424afea27e6420240206035357945213M",
            "title": "Docker 24.0.5```",
            "href": "/Docker 24.0.5```",
            "description": "\n@REM  Docker?\ncontainer를 다루는 사람\napp 구동에 필요한 모든 것을 container 에 넣어 급속냉동 시켜둔 것 같은 느낌\n최종 목표는 도커컨테이너\n\n@REM  check docker container console\ndocker logs 0707593299bf\n\n@REM  도커 장점\n쉽고 빠른 실행 환경 구축\n하드웨어 자원 절감\n\n리눅스  container 에 최적화된 platform.\nimage 하나로 server 복제 용이.\nauto scaling 으로 손쉽게 기능 확장 가능\nportable/lightweight\nimmutuable infrastructure\n\n@REM  도커 단점\n개발 초기의 오버헤드\n리눅스 만 친화적\n\n@REM 도커허브\nDocker Hub\n도커이미지 원격공유플랫폼\n\n@REM  docker 파일 생성\necho. >> web_server.Dockerfile\nsudo apt-get update\ncurl -sSL get.docker.com | sh\ndocker -v\n\n@REM  도커를 사용하려면 일부 권한 및 설정\n시스템그룹 docker로서 생성\n현사용자 docker에 추가\ndocker 그룹의 멤버들이 도커 소켓에 대해 쓰기가능 설정\n파일의 소유자를 root로, 그룹을 docker로 변경\nsudo addgroup --system docker\nsudo adduser $USER docker\nnewgrp docker\nsudo chown root:docker /var/run/docker.sock\n@REM  sudo chmod g+w /var/run/docker.sock\n\n@REM  프로젝트 디렉토리로 이동\ncd /mnt/e/PRJS_PRIVATE/prj_wsl+docker+node_js+express\n\n@REM  docker img 생성\nsudo docker build -f web_server.dockerfile -t img202311152342 ./\n\n@REM  실행가능한 docker img 를 출력 with container id\nsudo docker images\n\n@REM  모든 docker img  삭제\nsudo docker rmi $(sudo docker images -q) -f\n\n@REM  실행중인 docker container 를 출력\nsudo docker ps\nsudo docker ps | clip.exe\n\n@REM  실행중인 docker container 콘솔을 출력\nsudo docker logs 95488b494b95\n\n@REM  실행중인 모든 도커컨테이너 정지\nsudo docker stop $(sudo docker ps -qa)\n\n@REM  실행중인 모든 도커컨테이너 종료\nsudo docker kill $(sudo docker ps -qa)\n\n@REM  모든 도커컨테이너 삭제\nsudo docker rm -f $(sudo docker ps -qa)\n\nsudo docker logs $(sudo docker images -q)\n\ncd /mnt/e/PRJS_PRIVATE/prj_wsl+docker+node_js+express\n\n@REM docker exec\n이미 실행 중인 컨테이너에 접속하여 명령어를 실행할 수 있습니\ndocker exec -it 도커컨테이너ID echo \"test\"\n\n@REM  docker -e\n이 옵션은 Docker 컨테이너를 실행할 때 환경 변수를 설정하는 데 사용됩니다.\n환경 변수는 컨테이너 내에서 실행되는 애플리케이션에게 전달되는 변수입니다.\n이를 통해 애플리케이션의 동작을 구성하거나 설정가능\n\n@REM  docker license\n참고: Docker Desktop은 중소기업(직원 수 250명 미만 및 연간 매출 1,000만 달러 미만), 개인 용도, 교육 및 비상업적 오픈 소스 project 에 무료입니다.\n전문적인 사용을 위해 유료 구독이 필요합니다. 정부 기관에도 유료 구독이 필요합니다.\n\n@REM  docker container\n리눅스  안에서 다른 배포판의 리눅스 를 사용가능.\n\n@REM  korean environment\nCS(Desktop Application) 환경에서 program 은 window 기반이 대부분이다.\n특히 닷넷으로 window application 을 개발하려면 window OS 가 현재까지는 필수적이다.\n\n@REM  docker container virtual_box\nOS simulater\nvirtual IP\nvirtual memmory\n\n@REM  docker 는 hardware 가상화 가 아닌 hardware isolation 을 한다.\nit does not have hardware 가상화 계층.\nVM 에 비하여 월등히 빠르다.\n\n@REM  docker 과정\nbuild/ship/run\n\n@REM  docker file 저장소\ngit hub\n\n@REM  control 도커이미지\ndocker images\ndocker rmi\n\n@REM  control 도커컨테이너\ndocker rm\ndocker run\ndocker ps\ndocker exec\ndocker start\ndocker stop\ndocker attacch\ndocker load\ndocker save\n\n@REM  docker search ubuntu\n\n@REM  local volume mapping\nmemory resource 를 사용하려면 연결이 필요\n\n@REM  port forwarding\ndocker container 의 port 를 docker container 를 운영중인 OS 의 port 를 연결하는 듯.\n\n@REM 도커데몬 설치\n도커데스크탑에 도커데몬 내장\n    desktop 4.17.1 for windows\n        설치 중  h-HIVER 대신 WSL 2 로 DEFAULT 로서 가이드를 해주었음\n            explorer \"https://www.google.com/search?q=docker+desktop\"\n\n@REM 도커 버전 확인\ndocker -v\n    Docker version 20.10.23, build 7155243\n\n@REM  start docker deamon\nstart docker\n\n@REM  shutdown docker deamon\ntaskkill -f -im com.docker.service\n\n@REM  docker deamon\ndocker deamon 에서 docker container 를 실행 할 수 있는 것이다.\n\n@REM  docker container 실행\ndocker run --name img202311210000 -v -d nginx\ndocker run -d -p 80:80 -v ~/Desktop/test:/usr/local/apache2/htdocs/ img202311210000\ndocker start @REM  $(docker ps -qa) 를 응용가능하다고 한다\ndocker exec img202311210000 pwd\ndocker exec img202311210000 echo \"test\"\ndocker exec -it img202311210000 /bin/sh\ndocker exec -it img202311210000 /bin/sh exit;\n\n@REM  docker container 정보 확인\n$cat /etc/os-release\nNAME=\"CentOS 리눅스 \"\nVERSION=\"7 (Core)\"\nID=\"centos\"\nID_LIKE=\"rhel fedora\"\nVERSION_ID=\"7\"\nPRETTY_NAME=\"CentOS 리눅스  7 (Core)\"\nANSI_COLOR=\"0;31\"\nCPE_NAME=\"cpe:/o:centos:centos:7\"\nHOME_URL=\"https://www.centos.org/\"\nBUG_REPORT_URL=\"https://bugs.centos.org/\"\nCENTOS_MANTISBT_PROJECT=\"CentOS-7\"\nCENTOS_MANTISBT_PROJECT_VERSION=\"7\"\nREDHAT_SUPPORT_PRODUCT=\"centos\"\nREDHAT_SUPPORT_PRODUCT_VERSION=\"7\"\n\n\n@REM 도커데몬 실행\n:: 윈도우즈에서는 docker desktop 을 실행시켜야 한다. 그렇지 않으면 error during connect: This error may indicate that the docker daemon is not running.: Post~~~ 에러 나온다\n:: 자꾸 에러떠서 docker desktop 재설치 진행으로 해결했음.\n:: 깃 허브로 docker 로그인\ndocker login -u park4139\n도커허브인증토큰\n:: docker desktop 재실행\n\n\n@REM 모든 파이썬 패키지 삭제\nrun cmd.exe as admin\necho %cd% | clip\ncd C:\\projects\\services\\docker_image_maker\ncall \".venv\\Scripts\\activate.bat\"\npip freeze > server_fastapi_py_pkg_ver.log\necho y | pip uninstall -r server_fastapi_py_pkg_ver.log\ncall \".venv\\Scripts\\deactivate.bat\"\n\n@REM 모든 파이썬 패키지 재설치, jetbrain venv 연결이 invaild 인 경우\ncall \".venv\\Scripts\\deactivate.bat\"\necho y | rmdir /s \".venv\"\npython -m venv venv\ncall \".venv\\Scripts\\activate.bat\"\npip list\nrestart IDE\nalt enter 로 직접 패키지 수동 설치\n:: 패키지 수동 설치 결과 확인\ncall \".venv\\Scripts\\activate.bat\"\npip list\npython.exe -m pip install --upgrade pip\nconnect IDE python interpreter to this\nshift shift\npython interpreter\necho y | pip install -r server_fastapi_py_pkg_ver.log\npip list\npip freeze > server_fastapi_py_pkg_ver.log\ntype server_fastapi_py_pkg_ver.log\n\n@REM 도커이미지 빌드\ndocker build -t server_fastapi_image -f server_fastapi.Dockerfile . || wsl -e sh -c \"echo -e '\\033[0;31m도커이미지 빌드 실패\\033[0m';\" && timeout 600 > nul\ndocker image ls\n\n@REM 도커컨테이너 실행 via interactive mode\ndocker run -it --name server_fastapi_container -p 8080:80 server_fastapi_image:latest\n\n@REM 도커컨테이너 실행 as service without detached mode\ndocker run --name server_fastapi_container -p 8080:80 server_fastapi_image:latest\n\n@REM 도커컨테이너 실행 as service with detached mode\ndocker run -d --name server_fastapi_container -p 8080:80 server_fastapi_image:latest\n:: -d Detached 모드(백그라운드 모드)\n:: -v [호스트 디렉토리]:[컨테이너 디렉토리] 호스트의 디렉토리와 컨테이너의 디렉토리를 공유\n\n@REM get request 테스트 as CLI, Fastapi swagger UI로 귀찮을 때\nexplorer http://localhost:8080/docs\nexplorer http://localhost:8080/nav-items/0\n\n@REM 실행된 도커컨테이너 에 명령 via interactive mode\nls\n:: # alpine 리눅스  머신에 설치가능한 python3 최신 버전 확인\napk policy python3\npython --version\npython3 --version\npip --version\npip3 --version\n:: apt-get install python3.12-dev\n:: python3.12 -m pip install --upgrade setuptools\n:: python3 -m ensurepip --upgrade\n:: python3 get-pip.py\n:: python3 -m pip.pyz --help\n:: pip install --upgrade setuptools\n:: pip install --no-cache-dir --upgrade -r /code/py_pkg_ver_for_리눅스 .log\nexit\n@rem 도커컨테이너 수행내용 새로운이미지에 저장\ndocker commit 컨테이너ID 새로운이미지명\n\n@REM 도커컨테이너 확인(실행중인)\ndocker ps\n\n@REM 도커컨테이너 확인(모든)\ndocker ps -a\n\n@REM 특정 도커컨테이너 실행(attached mode, interactive mode)\ndocker ps -a\nsudo docker ps -a\ndocker start -ai 도커컨테이너ID\ndocker start -ai 8023fdeeae56\nsudo docker start -ai 8023fdeeae56\n\n@REM 도커컨테이너 중지/삭제\ndocker container ls -a | findstr server_alpine_container\ndocker container ls -a | clip\ndocker stop 도커컨테이너ID\ndocker stop 8023fdeeae56\ndocker rm 도커컨테이너ID\ndocker rm 8023fdeeae56\ndocker container ls -a\ndocker ps -a\n\n@REM 도커이미지 삭제\n:: docker rmi $(docker images -q)   리눅스  용\ndocker image ls | clip\ndocker rmi 도커이미지ID\ndocker rmi ef3c64bd5725\ndocker image ls\n\n@REM 도커이미지 빌드 프로젝트 PUSH (to 깃허브)\nset commit_ment=fastapi 서버 도커파일 local test 완료\nset commit_ment=alpine 리눅스  로 컨버팅 중인 커스텀 패키지\nset commit_ment=alpine 리눅스  기반 fastapi 서버 도커파일 local test 완료\nset commit_ment=alpine 리눅스  기반 파이썬 도커이미지 PUSH 완료(도커허브로)\nset commit_ment=fastapi 엔드포인트 업데이트\ngit add *\ngit commit -m \"%commit_ment%\"\ngit push -u origin main\ngit status | find \"working tree clean\"\n\n\n@REM 도커이미지 PUSH (to 도커허브)\ndocker logs -f 도커컨테이너ID\n:: 도커이미지 PUSH 전 도커이미지명 레파지토리와 연동되도록 설정\ndocker tag server_fastapi_image park4139/server_fastapi_image\n:: 도커이미지 PUSH\ndocker push park4139/server_fastapi_image\n\n@REM 도커허브 내 도커이미지 최신화 루틴\ndocker image ls\ndocker image ls | clip\ndocker rmi de6f37092f26\ndocker ps\ndocker ps -a\ndocker build -t server_fastapi_image -f server_fastapi.Dockerfile . || wsl -e sh -c \"echo -e '\\033[0;31m도커이미지 빌드 실패\\033[0m';\" && timeout 600 > nul\ndocker tag server_fastapi_image park4139/server_fastapi_image\ndocker image ls\ndocker push park4139/server_fastapi_image\n\n"
        },
        {
            "index": "e59815170829463eae82ae33a27f746520240206175805388909X",
            "title": "Uvicorn 0.27.0```",
            "href": "/Uvicorn 0.27.0```",
            "description": "\n# Uvicorn?\nWeb Server/WAS 역할 수행\n비동기 애플리케이션을 실행하고 관리하는 데 효율적.\nPython으로 개발됨, 파이썬과 호환성이 좋음\nASGI 프로토콜을 지원하여 비동기적(asynchronous) 으로 request(요청)을 처리하고 응답을 반환합니다.\nASGI 애플리케이션을 실행, request(요청)를 asynchronous 방식으로 처리 및 forwarding 역할 수행.\nresponse return 역할 수행\nuvicorn 포트 설정 지원(previlleged ports 제외)\n\n# ASGI\nAsynchronous Server Gateway Interface\n비동기처리\n비동기 웹 애플리케이션은 ASGI 애플리케이션 일수 있다.\nfastapi로 많이 구성한다.\n\n# WSGI\nweb Server Gateway Interface\n동기처리\n\n"
        },
        {
            "index": "72915e68e7f94ab3bd7e4828b3c7164d20240206182115656353s",
            "title": "FastAPI 0.109.0```",
            "href": "/FastAPI 0.109.0```",
            "description": "\n# FastAPI?\nFastAPI 내에서 routing 되어 fastapi 에 정의된 end point에 도달하여 동적 request 를 처리 후 return\nASGI 지원\n\n# FastAPI 철학\nHigh Performance\nEasy to Learn\nFast to Code\nReady for Production\n\n# FastAPI Starlette\nStarlette(https://github.com/enode/starlette) 프레임 워크를 기반으로한 비동기 API 서버 지원\n\n# FastAPI ASGI \nASGI 사용으로 FastAPI 안에서 비동기 처리를 수행\n\n# FastAPI performance test\n성능과 부하 test 에서 상위 랭커로서 결과를 내고 있음\n\n# FastAPI Pydantic\n데이터 밸리데이션 지원\nPydantic 은 현존 python 벨리데이터 중 가장 빠름.\nPydantic 으로 간결한 데이터 벨리데이션 가능.\n덧붙여, Django도 3.x대 버전으로 이상에서 @sync_to_async 데코레이터/async/await 조합으로 비동기 구현 가능\n\n# FastAPI API Swagger\nOpenAPI를 사용하여 자동으로 생성되는 API Swagger\n풀스택 개발이 아닌 프론트와 백으로 역할 분담하여 개발진행되는 팀의 경우 API Swagger 굉장히 유용\nOpenAPI 문서 자동생성. 개발자가 작성해야하는 API 문서를 자동생성.\n\n# FastAPI 공식문서\n맥락을 설명해주며 설명하는 상세한 공식문서\n\n"
        }
    ]
    with open(NAV_ITEMS_JSON, "w", encoding="utf-8") as file:
        json.dump(dummy_data, file)
        # json.dump(dummy_data, file, ensure_ascii=False)
    DebuggingUtil.print_magenta(f"더미를 {dummy_cnt} 개로 리셋하였습니다")
    return dummy_data


@router.get("/nav-items")
def get_nav_items():
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    # NAV_ITEMS = FastapiUtil.init_and_update_json_file(StateManagementUtil.NAV_ITEMS_JSON)
    with open(StateManagementUtil.NAV_ITEMS_JSON, "r", encoding="utf-8") as file:
        NAV_ITEMS = json.load(file)
    [print(sample) for sample in NAV_ITEMS]
    return NAV_ITEMS


@router.get("/nav-items/{index}")
def get_nav_items_by_index(index: str):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    # NAV_ITEMS = FastapiUtil.init_and_update_json_file(StateManagementUtil.NAV_ITEMS_JSON)
    try:
        with open(StateManagementUtil.NAV_ITEMS_JSON, "r", encoding="utf-8") as file:
            NAV_ITEMS = json.load(file)
        return NAV_ITEMS[int(index)]
    except:
        DebuggingUtil.print_ment_fail(f"({len(NAV_ITEMS)})개의 등록된 nav_items 중, index 가 {index}인 nav_item 이 없습니다.")
        raise HTTPException(status_code=404, detail=f"({len(NAV_ITEMS)})개의 등록된 nav_items 중, index 가 {index}인 nav_item 이 없습니다.")
