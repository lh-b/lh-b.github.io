(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[166],{3175:function(e,t,r){"use strict";r.r(t);var n=r(5893),i=r(7294),s=r(1166),a=[{id:"1",type:"Disc",title:"Macintosh HD"},{id:"2",type:"Folder",title:"Big Sur"},{id:"3",type:"PDF",title:"Menual.pdf"}];t.default=function(){var e=(0,i.useState)(""),t=e[0],r=e[1],o=(0,i.useContext)(s.AppContext).updateDesktopClickHash,l=function(e,t){var r="";switch(e){case"Folder":r="/images/folder-icon.png";break;case"Disc":r="/images/disk-icon.png";break;case"PDF":r="/images/pdf-icon.png"}return(0,n.jsx)("div",{className:"image-wrapper rounded-md border-2 border-transparent border-box px-1 py-2 ".concat(t?"bg-gray-900 border-gray-500 bg-opacity-30":""),children:(0,n.jsx)("img",{alt:"select-none dock item logo",className:"w-12",src:r})})};return(0,n.jsx)("div",{className:"flex flex-col items-end fixed left-0 top-0 h-screen w-screen border-box pt-6",onClick:function(){r(""),o()},children:a.map((function(e,i){return(0,n.jsxs)("button",{"data-testid":"desktop-item-".concat(i+1),className:"w-32 flex flex-col items-center my-2 p-1",onClick:function(t){return function(e,t){e.stopPropagation(),r(t),o()}(t,e.id)},children:[l(e.type,t===e.id),(0,n.jsx)("h3",{className:"select-none text-xs text-white font-bold whitespace-nowrap text-center mt-0.5 text-shadow-sm pl-2 pr-2 pt-0.5 pb-0.5 rounded-md".concat(t===e.id?" bg-blue-700":""),children:e.title})]},e.id)}))})}},9492:function(e,t,r){"use strict";r.r(t);var n=r(5893),i=r(7294),s=r(1166),a=[{title:"Finder",logo:"images/finder-logo.png"},{title:"Safari",logo:"images/safari-logo.png"},{title:"Messages",logo:"images/messages-logo.png"},{title:"Music",logo:"images/music-logo.png"},{title:"Mail",logo:"images/mail-logo.png"},{title:"Photos",logo:"images/photos-logo.png"},{title:"Contacts",logo:"images/contacts-logo.png"},{title:"Calendar",logo:"images/calendar-logo.png"},{title:"Stocks",logo:"images/stocks-logo.png"},{title:"Facetime",logo:"images/facetime-logo.png"},{title:"Maps",logo:"images/maps-logo.png"},{title:"Note",logo:"images/note-logo.png"},{title:"Settings",logo:"images/settings-logo.png"},{title:"Reminders",logo:"images/reminders-logo.png"},{title:"News",logo:"images/news-logo.png"}];t.default=function(){var e=(0,i.useRef)(),t=(0,i.useContext)(s.AppContext).updateDesktopClickHash;return(0,n.jsx)("div",{ref:e,className:"flex h-16 flex-row justify-center items-end bg-white fixed bottom-2 left-0 right-0 px-2 bg-opacity-10 w-max m-auto rounded-xl",children:a.map((function(r,i){return(0,n.jsx)("button",{className:"w-16 align-bottom dock-item p-2",style:{transition:"all ease .2s"},onMouseEnter:function(){return t=i,e.current.children[t].style.width="".concat(8,"rem"),t>0&&e.current.children[t-1]&&(e.current.children[t-1].style.width="".concat(6.5,"rem")),t>0&&e.current.children[t-2]&&(e.current.children[t-2].style.width="".concat(5.5,"rem")),t<a.length-1&&e.current.children[t+1]&&(e.current.children[t+1].style.width="".concat(6.5,"rem")),void(t<a.length-1&&e.current.children[t+2]&&(e.current.children[t+2].style.width="".concat(5.5,"rem")));var t},onMouseLeave:function(){return t=i,e.current.children[t].style.width="".concat(4,"em"),t>0&&e.current.children[t-1]&&(e.current.children[t-1].style.width="".concat(4,"em")),t>0&&e.current.children[t-2]&&(e.current.children[t-2].style.width="".concat(4,"em")),t<a.length-1&&e.current.children[t+1]&&(e.current.children[t+1].style.width="".concat(4,"em")),void(t<a.length-1&&e.current.children[t+2]&&(e.current.children[t+2].style.width="".concat(4,"em")));var t},onClick:function(){t()},children:(0,n.jsx)("img",{alt:"dock icon",className:"select-none w-full",src:r.logo})},r.title)}))})}},5823:function(e,t,r){"use strict";r.r(t);var n=r(5893);t.default=function(e){var t=e.items,r=e.title;return(0,n.jsx)("div",{className:"absolute bg-gray-700 bg-opacity-50 p-1 rounded-md left-0 border border-gray-500 border-box".concat("Apple"===r?" top-5":""),children:t&&t.map((function(e){return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("a",{className:"text-white px-2 py-0.5 text-sm whitespace-nowrap text-left rounded-md w-full block hover:bg-blue-600",children:(0,n.jsxs)("p",{className:"flex justify-between",children:[(0,n.jsx)("span",{className:"",children:e.title}),(0,n.jsx)("span",{className:"text-gray-400 ml-16",children:e.rightLabel})]})},e.title),e.separator&&(0,n.jsx)("span",{className:"block h-0.5 border-b border-gray-500 my-1 mx-2 text-xs"})]})}))})}},1453:function(e,t,r){"use strict";r.r(t);var n=r(5893),i=r(7294),s=r(381),a=r.n(s),o=r(1166),l=r(5823),c=["File","Edit","View","Go","Window","Help"];t.default=function(){var e=(0,i.useState)(""),t=e[0],r=e[1],s=(0,i.useState)(""),u=s[0],d=s[1],p=(0,i.useState)(""),m=p[0],g=p[1],f=(0,i.useContext)(o.AppContext),h=f.desktopClickHash,x=f.updateDesktopClickHash;return(0,i.useEffect)((function(){var e=function(){var e=a()(),t=e.format("dddd").substring(0,3),r=e.format("MMM").substring(0,3),n=e.format("DD"),i="".concat(t," ").concat(r," ").concat(n);g((function(e){return e!==i?i:e}))},t=function(){var e=a()(),t=e.format("hh").substring(0,3),r=e.format("mm").substring(0,3),n=e.format("A"),i="".concat(t,":").concat(r," ").concat(n);d((function(e){return e!==i?i:e}))};e(),t(),setInterval((function(){e(),t()}),1e3)}),[]),(0,i.useEffect)((function(){r("")}),[h]),(0,n.jsxs)("div",{onClick:x,className:"border-box flex flex-row justify-between w-screen h-6 bg-gray-600 fixed top-0 left-0 bg-opacity-40 border-b border-gray-500 z-10",children:[(0,n.jsxs)("div",{className:"flex items-center",children:[(0,n.jsxs)("button",{className:"pl-4 pr-1 ml-1.5 rounded-sm relative cursor-pointer",onClick:function(e){e.stopPropagation(),r((function(e){return"Apple"!==e?"Apple":""}))},onMouseEnter:function(){t&&"Apple"!==t&&r("Apple")},children:[(0,n.jsx)("img",{alt:"apple icon",className:"w-3.5",src:"images/apple-logo.png"}),"Apple"===t&&(0,n.jsx)(l.default,{title:t,items:[{title:"About This Mac",separator:!0,rightLabel:""},{title:"System Preferences",separator:!1,rightLabel:""},{title:"App Store...",separator:!0,rightLabel:"8 updates"},{title:"Recent Items",separator:!0,rightLabel:""},{title:"Force Quit",separator:!0,rightLabel:"\u2325\u2318\u238b"},{title:"Sleep",separator:!1,rightLabel:""},{title:"Restart...",separator:!1,rightLabel:""},{title:"Shut Down...",separator:!0,rightLabel:""},{title:"Lock Screen",separator:!1,rightLabel:"^\u2318Q"},{title:"Log Out Soroush...",separator:!1,rightLabel:"\u21e7\u2318Q"}]})]}),(0,n.jsxs)("button",{className:"pl-4 relative",onClick:function(e){e.stopPropagation(),r((function(e){return"Finder"!==e?"Finder":""}))},onMouseEnter:function(){t&&"Finder"!==t&&r("Finder")},children:[(0,n.jsx)("span",{className:"font-bold text-white text-sm",children:"Finder"}),"Finder"===t&&(0,n.jsx)(l.default,{title:t,items:[{title:"About Finder",separator:!0,rightLabel:""},{title:"Preferences...",separator:!0,rightLabel:"\u2318 ,"},{title:"Empty Trash...",separator:!0,rightLabel:"\u21e7\u2318\u232b"},{title:"Services",separator:!0,rightLabel:""},{title:"Hide Finder",separator:!1,rightLabel:"\u2318H"},{title:"Hide Others",separator:!1,rightLabel:"\u2325\u2318H"},{title:"Show All",separator:!1,rightLabel:""}]})]}),(0,n.jsx)("div",{children:c.map((function(e){return(0,n.jsxs)("button",{className:"pl-5 text-sm relative",onClick:function(t){t.stopPropagation(),r((function(t){return t!==e?e:""}))},onMouseEnter:function(){t&&t!==e&&r(e)},children:[(0,n.jsx)("span",{className:"text-white",children:e}),t===e&&(0,n.jsx)(l.default,{title:t,items:[{title:"About ".concat(e),separator:!0,rightLabel:""},{title:"Preferences...",separator:!1,rightLabel:"\u2318P".concat(e.split("")[0])}]})]},e)}))})]}),(0,n.jsxs)("div",{className:"flex flex-row justify-center items-center",children:[(0,n.jsx)("button",{className:"w-8 h-5 mr-5 mt-0.5",children:(0,n.jsx)("img",{alt:"menubar icon",className:"w-full h-full",src:"/images/battery-icon.png"})}),(0,n.jsx)("button",{className:"w-4 mr-5",children:(0,n.jsx)("img",{alt:"menubar icon",className:"w-full",src:"/images/wifi-icon.png"})}),(0,n.jsx)("button",{className:"w-4 mr-5",children:(0,n.jsx)("img",{alt:"menubar icon",className:"w-full",src:"/images/magnifier-icon.png"})}),(0,n.jsx)("button",{className:"w-3.5 mr-5",children:(0,n.jsx)("img",{alt:"menubar icon",className:"w-full",src:"/images/control-center-icon.png"})}),(0,n.jsx)("button",{className:"w-3.5 mr-5",children:(0,n.jsx)("img",{alt:"menubar icon",className:"w-full",src:"/images/siri-logo.png"})}),(0,n.jsxs)("button",{className:"flex flex-row justify-center items-center",children:[(0,n.jsx)("p",{className:"text-sm text-white mr-2",children:m}),(0,n.jsx)("p",{className:"text-sm text-white mr-5",children:u})]})]})]})}},1166:function(e,t,r){"use strict";r.r(t),r.d(t,{AppContext:function(){return b},default:function(){return w}});var n,i=r(5893),s=r(7294),a=r(9008),o=new Uint8Array(16);function l(){if(!n&&!(n="undefined"!==typeof crypto&&crypto.getRandomValues&&crypto.getRandomValues.bind(crypto)||"undefined"!==typeof msCrypto&&"function"===typeof msCrypto.getRandomValues&&msCrypto.getRandomValues.bind(msCrypto)))throw new Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");return n(o)}var c=/^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;for(var u=function(e){return"string"===typeof e&&c.test(e)},d=[],p=0;p<256;++p)d.push((p+256).toString(16).substr(1));var m=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0,r=(d[e[t+0]]+d[e[t+1]]+d[e[t+2]]+d[e[t+3]]+"-"+d[e[t+4]]+d[e[t+5]]+"-"+d[e[t+6]]+d[e[t+7]]+"-"+d[e[t+8]]+d[e[t+9]]+"-"+d[e[t+10]]+d[e[t+11]]+d[e[t+12]]+d[e[t+13]]+d[e[t+14]]+d[e[t+15]]).toLowerCase();if(!u(r))throw TypeError("Stringified UUID is invalid");return r};var g=function(e,t,r){var n=(e=e||{}).random||(e.rng||l)();if(n[6]=15&n[6]|64,n[8]=63&n[8]|128,t){r=r||0;for(var i=0;i<16;++i)t[r+i]=n[i];return t}return m(n)},f=r(1453),h=r(9492),x=r(3175),b=(0,s.createContext)({desktopClickHash:"",updateDesktopClickHash:function(){}}),w=function(){var e=(0,s.useState)(g()),t=e[0],r=e[1];return(0,i.jsxs)(b.Provider,{value:{desktopClickHash:t,updateDesktopClickHash:function(){r(g())}},children:[(0,i.jsx)(a.default,{children:(0,i.jsx)("title",{children:"macOS Big Sur"})}),(0,i.jsxs)("div",{className:"flex mx-auto w-screen h-screen bg-wallpaper bg-cover overflow-hidden",children:[(0,i.jsx)(f.default,{}),(0,i.jsx)(x.default,{}),(0,i.jsx)(h.default,{})]})]})}},9008:function(e,t,r){e.exports=r(639)}}]);
