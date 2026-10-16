# 路由映射（源码轮次）

- 目标：`https://screen.sessionhd.com/screen/index.html?preview=browser&type=default#/3d`
- 分析日期：2026-10-16
- 来源：`evidence/02-baseline/assets/index.29842956.js`
- router：vue-router 3.6.5；mode=`hash`；base=`https://static.newstartjx.com/screen/app/`
- 路由对象数：84（含默认 `path:"", name:"Home"`）

## 行为

- 默认路由：`#/` -> `Home`，模块 `bb51`，chunk `chunk-2c7cb330`。
- `beforeEach`：未匹配路由重定向到 `/`。
- 已匹配路由还需满足：在 `activityHudongList` 中 `status === "1"`，或属于 `""`、`signin`、`setting`、`barrage` 白名单；否则重定向到 `/`。
- 懒加载：路由组件通过 webpack `n.e("chunk-...")` 加载，再 `n.bind(null, entryModule)`。
- query：预览失败回跳逻辑读取 `location.search` 的 `preview`、`cid`、`uid`，并从 hash 中拆分 `frame` 与附加 query。

## 路由表

| # | path | name | entry module | lazy chunks |
|---:|---|---|---|---|
| 1 | `/barrage` | `Barrage` | `e049` | `chunk-a6b81ef8` |
| 2 | `` | `Home` | `bb51` | `chunk-2c7cb330` |
| 3 | `/setting` | `Setting` | `bb51` | `chunk-2c7cb330` |
| 4 | `/launching` | `Launching` | `3f70` | `chunk-ac4e4a3c`, `chunk-3ec527c9` |
| 5 | `/countdown` | `Countdown` | `8bdf` | `chunk-23185731` |
| 6 | `/writing` | `Writing` | `44d7` | `chunk-e31950d6`, `chunk-2064b242`, `chunk-24f83a56`, `chunk-2cc94003` |
| 7 | `/book` | `Book` | `a001` | `chunk-e2581cca` |
| 8 | `/signin` | `Signin` | `9f3e` | `chunk-c2807904`, `chunk-a0be740e` |
| 9 | `/3d` | `3d` | `78f0` | `chunk-e31950d6`, `chunk-c2807904`, `chunk-2064b242`, `chunk-5df911d3`, `chunk-9aaf1298` |
| 10 | `/annual` | `Annual` | `c674` | `chunk-e31950d6`, `chunk-2064b242`, `chunk-5df911d3`, `chunk-dafc189a` |
| 11 | `/mosaic` | `Mosaic` | `ec6d` | `chunk-c2807904`, `chunk-03993300` |
| 12 | `/logo` | `Logo` | `5569` | `chunk-c2807904`, `chunk-ee03ff1a` |
| 13 | `/tree` | `Tree` | `5eb6` | `chunk-2a4fe9ac` |
| 14 | `/area` | `Area` | `20d0` | `chunk-b6b446d6` |
| 15 | `/tapho` | `Tapho` | `e1ae` | `chunk-e31950d6`, `chunk-c2807904`, `chunk-2064b242`, `chunk-5df911d3`, `chunk-793e316c` |
| 16 | `/wall` | `Wall` | `901a` | `chunk-9c493a18` |
| 17 | `/match` | `Match` | `0925` | `chunk-76e3dcad`, `chunk-3e2da3a0`, `chunk-6060ec36` |
| 18 | `/faq` | `Faq` | `7f99` | `chunk-f2df9670` |
| 19 | `/honored` | `Honored` | `e9e28` | `chunk-76e3dcad`, `chunk-33602305` |
| 20 | `/wish` | `Wish` | `9ade` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-7e18f80c`, `chunk-5cc1e0a8` |
| 21 | `/contract` | `Contract` | `4f78` | `chunk-24f83a56`, `chunk-33407a42` |
| 22 | `/vote` | `Vote` | `7175` | `chunk-76e3dcad`, `chunk-2621d2be`, `chunk-d8d3d554` |
| 23 | `/grade` | `Grade` | `ad4f` | `chunk-76e3dcad`, `chunk-389c50db` |
| 24 | `/target` | `Target` | `2c61` | `chunk-078d9814`, `chunk-4f1cca0b` |
| 25 | `/opinion` | `Opinion` | `62c2` | `chunk-196c683c` |
| 26 | `/ballot` | `Ballot` | `c8b5` | `chunk-76e3dcad`, `chunk-2621d2be`, `chunk-20160981` |
| 27 | `/rain` | `Rain` | `72aa` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d0d6931` |
| 28 | `/scratch` | `Scratch` | `2346` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d0b2179` |
| 29 | `/shake` | `Shake` | `3c69` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d0c4a49` |
| 30 | `/dice` | `Dice` | `c701` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d21762b` |
| 31 | `/voice` | `Voice` | `da0d` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d228867` |
| 32 | `/hunter` | `Hunter` | `d1db` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d21da81` |
| 33 | `/scan` | `Scan` | `a9a2` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d209adf` |
| 34 | `/firework` | `Firework` | `bd9d` | `chunk-78e60109`, `chunk-33f2f709`, `chunk-2d21ac03` |
| 35 | `/avatar` | `Avatar` | `551a` | `chunk-76e3dcad`, `chunk-7e18f80c`, `chunk-4ee9b42a` |
| 36 | `/name` | `Name` | `2a04` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-7e18f80c`, `chunk-4c0f556c`, `chunk-c27af9ba` |
| 37 | `/tiger` | `Tiger` | `86e9` | `chunk-76e3dcad`, `chunk-046bb27d`, `chunk-06416769` |
| 38 | `/listdraw` | `Listdraw` | `a394` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-7e18f80c`, `chunk-332ce0cf`, `chunk-30ec0897` |
| 39 | `/photodraw` | `Photodraw` | `84b6` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-7e18f80c`, `chunk-625cce37` |
| 40 | `/seatdraw` | `Seatdraw` | `67e8` | `chunk-76e3dcad`, `chunk-7e18f80c`, `chunk-332ce0cf`, `chunk-0f89a7cd` |
| 41 | `/tornado` | `Tornado` | `f339` | `chunk-76e3dcad`, `chunk-046bb27d`, `chunk-2a98b71a` |
| 42 | `/three` | `Three` | `4643` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-7e18f80c`, `chunk-40f2b7fe` |
| 43 | `/lamp` | `Lamp` | `8ae1` | `chunk-76e3dcad`, `chunk-7e18f80c`, `chunk-06357962` |
| 44 | `/single` | `Single` | `b514` | `chunk-76e3dcad`, `chunk-7e18f80c`, `chunk-984e4d10` |
| 45 | `/blessdraw` | `Blessdraw` | `e80f` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-7e18f80c`, `chunk-2b0a4b23` |
| 46 | `/danmaku` | `Danmaku` | `7c49` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-7e18f80c`, `chunk-af0d8374` |
| 47 | `/lotdraw` | `Lotdraw` | `2c55` | `chunk-76e3dcad`, `chunk-e31950d6`, `chunk-3e2da3a0`, `chunk-0efaafc6` |
| 48 | `/welfare` | `Welfare` | `632e` | `chunk-598480ad` |
| 49 | `/ticketdraw` | `Ticketdraw` | `2dad` | `chunk-76e3dcad`, `chunk-7e18f80c`, `chunk-4c0f556c`, `chunk-095a861c` |
| 50 | `/picture` | `Picture` | `ae3a` | `chunk-e31950d6`, `chunk-b1e622d4` |
| 51 | `/tugofwar` | `Tugofwar` | `b185` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-5731daba` |
| 52 | `/money` | `Money` | `8b43` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-07234966` |
| 53 | `/lrclick` | `Lrclick` | `0195` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-5610a872` |
| 54 | `/horizontal` | `Horizontal` | `0f83` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-0c052d1e` |
| 55 | `/energybar` | `Energybar` | `0496` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-191bff6e` |
| 56 | `/vertical` | `Vertical` | `edc6` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-b226113c` |
| 57 | `/lightup` | `Lightup` | `6623` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-68257a8e` |
| 58 | `/shoot` | `Shoot` | `c841` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-426bb33d` |
| 59 | `/slice` | `Slice` | `9700` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-6ff218ba` |
| 60 | `/beat` | `Beat` | `ff64` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-4eadfeb1` |
| 61 | `/jumping` | `Jumping` | `c5d7` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-a0543456` |
| 62 | `/puzzle` | `Puzzle` | `ba1f` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-00aaa3a6` |
| 63 | `/points` | `Points` | `2353` | `chunk-76e3dcad`, `chunk-7f2584f0`, `chunk-5feb2264` |
| 64 | `/rhythm` | `Rhythm` | `b935` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-55e7e63a` |
| 65 | `/answer` | `Answer` | `26db` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-19af2998` |
| 66 | `/ccard` | `Ccard` | `374a` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-4a6c95ff` |
| 67 | `/sing` | `Sing` | `86cd` | `chunk-533d7afd` |
| 68 | `/boomy` | `Boomy` | `769c` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-194f4357` |
| 69 | `/hecombine` | `Hecombine` | `d797` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-d00dda44` |
| 70 | `/circletouch` | `Circletouch` | `ff88` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-443df8a2` |
| 71 | `/lrslide` | `Lrslide` | `3762` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-6637b162` |
| 72 | `/sale` | `Sale` | `6c5d` | `chunk-078d9814`, `chunk-3ecdc904` |
| 73 | `/lucky` | `Lucky` | `d6a6` | `chunk-38202c12`, `chunk-2dd5bf61` |
| 74 | `/box` | `Box` | `d5b0` | `chunk-5390cc9b` |
| 75 | `/pachinko` | `Pachinko` | `5bda` | `chunk-38202c12`, `chunk-5b9a01a0` |
| 76 | `/auction` | `Auction` | `3cd0` | `chunk-76e3dcad`, `chunk-c172cf5a` |
| 77 | `/act` | `Act` | `6207` | `chunk-76e3dcad`, `chunk-0b65c4ae` |
| 78 | `/dedicate` | `Dedicate` | `ec4b` | `chunk-26b5f027` |
| 79 | `/rush` | `Rush` | `5cc5` | `chunk-76e3dcad`, `chunk-7f2584f0`, `chunk-a461472e` |
| 80 | `/sport` | `Sport` | `bfbd` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-9ee9f8ae` |
| 81 | `/eliminate` | `Eliminate` | `3691` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-c80dfa02` |
| 82 | `/ranking` | `Ranking` | `08f9` | `chunk-76e3dcad`, `chunk-78e60109`, `chunk-7f2584f0`, `chunk-6249c944`, `chunk-0286bc29` |
| 83 | `/leave` | `Leave` | `600c` | `chunk-e31950d6`, `chunk-c2807904`, `chunk-1e887133` |
| 84 | `/richtext` | `Richtext` | `e7c5` | `chunk-e31950d6`, `chunk-c2807904`, `chunk-7fb74269` |

## 证据与缺口

- 源码证据：所有路由对象和懒加载 chunk 来自上述 app bundle；机器可读版本见 `route-map.json`。
- 网络证据：`runtime-probe.json` 记录 `/3d` 加载了 `chunk-e31950d6`、`chunk-c2807904`、`chunk-2064b242`、`chunk-5df911d3`、`chunk-9aaf1298`，与源码一致。
- 截图证据：**待验证（纯源码轮次）**。未对 84 条路由逐条截图，也未验证活动配置动态启用的白名单位。
- 因每条路由的截图/网络证据验收未完成，P4-02 不标记为 done。
