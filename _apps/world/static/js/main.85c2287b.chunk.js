(this["webpackJsonpdev-pages"]=this["webpackJsonpdev-pages"]||[]).push([[0],{117:function(t,n,e){},119:function(t,n,e){"use strict";e.r(n);var o=e(10),a=e(6),r=e(47),i=e(31),c=e.n(i),g=e(53),u=e.p+"static/media/earth-blue-marble.7deee995.jpg",l=e.p+"static/media/night-sky.51b096ab.png",p=e.p+"static/media/earth-topology.739e278b.png",s=e.p+"static/media/minimal_countries.2e612b23.geojson",b=e(54),P=(e(117),e(26));function O(){var t=Object(a.useState)({features:[]}),n=Object(o.a)(t,2),e=n[0],i=n[1],c=Object(a.useState)(),O=Object(o.a)(c,2),_=O[0],f=O[1],d=b.a().domain([0,5e3]).range(["rgba(173, 216, 230, 0.5)","rgba(139, 0, 0, 0.8)"]).clamp(!0);return Object(a.useEffect)((function(){fetch(s).then((function(t){return t.json()})).then(i)}),[]),Object(P.jsx)(r.SizeMe,{monitorHeight:!0,children:function(t){var n=t.size;return Object(P.jsx)(g.a,{width:n.width,globeImageUrl:u,bumpImageUrl:p,backgroundImageUrl:l,onPolygonHover:f,polygonsData:e.features.filter((function(t){return t.properties.MtCO2_EST})),polygonsTransitionDuration:300,polygonAltitude:function(t){return t===_?.02:.01},polygonCapColor:function(t){var n=t.properties;return d(n.MtCO2_EST)},polygonSideColor:function(t){var n=t.properties;return d(n.MtCO2_EST)},polygonStrokeColor:function(){return"rgba(255, 255, 255, 0.1)"},polygonLabel:function(t){var n=t.properties;return"\n          <b>".concat(n.NAME_KR," (").concat(n.ISO_A2,")</b> <br>\n          \ud0c4\uc18c\ubc30\ucd9c\ub7c9: <i>").concat(n.MtCO2_EST.toLocaleString(navigator.language),"MtCO2 (").concat(n.MtCO2_YEAR,")</i> <br>\n          \uc778\uad6c\uc218: <i>").concat(n.POP_EST.toLocaleString(navigator.language),"\uba85 (").concat(n.POP_YEAR,")</i> <br>\n          \uc778\uad6c \uc21c\uc704: <i>").concat(n.POP_RANK,"</i> <br>\n          1\uc778\ub2f9 GDP(nominal): <i>").concat(n.GDP_NOMINAL_EST.toLocaleString(navigator.language)," (").concat(n.GDP_NOMINAL_YEAR,")</i> <br>\n          1\uc778\ub2f9 GDP(PPP): <i>").concat(n.GDP_PPP_EST.toLocaleString(navigator.language)," (").concat(n.GDP_PPP_YEAR,")</i> <br>\n        ")}})}})}c.a.render(Object(P.jsx)(O,{}),document.getElementById("root"))}},[[119,1,2]]]);
//# sourceMappingURL=main.85c2287b.chunk.js.map