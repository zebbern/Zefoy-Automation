(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push(["object" == typeof document ? document.currentScript : undefined, 50308, e => {
    "use strict";
    var t = e.i(91398);
    e.s(["default", 0, function({
        children: e,
        className: r,
        variant: i = "default"
    }) {
        return (0, t.jsx)("div", {
            className: `${{default: "px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto", hero: "px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto", narrow: "px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto"}[i]} ${r || ""}`,
            children: e
        });
    }]);
}, 7293, e => {
    "use strict";
    var t = e.i(91398),
        r = e.i(41158),
        i = e.i(50308),
        o = e.i(91788);

    function n() {
        let e = (0, o.useRef)(null);
        return (0, o.useEffect)(() => {
            let t = setTimeout(() => {
                window.nitroAds && window.nitroAds.loaded && (e.current.style.display = window.__tcfapi ? "block" : "none");
            }, 3e3);
            return () => {
                clearTimeout(t);
            };
        }, []), (0, t.jsx)("button", {
            ref: e,
            className: "dark:text-zinc-300 dark:bg-black text-zinc-500 text-sm hidden",
            onClick: () => window && window.__cmp && "function" == typeof window.__cmp && window.__cmp("showModal"),
            children: "Update cookie preferences"
        });
    }
    e.s(["default", 0, function({
        service: e
    }) {
        return (0, t.jsx)("footer", {
            className: "relative py-16 dark:bg-black",
            children: (0, t.jsx)(i.default, {
                className: "relative z-10",
                children: (0, t.jsxs)("div", {
                    className: "space-y-8",
                    children: [e && (0, t.jsx)("div", {
                        className: "text-center p-6 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10",
                        children: (0, t.jsxs)("p", {
                            className: "text-sm text-zinc-500 dark:text-zinc-300 leading-relaxed",
                            children: ["The public statistical data is sourced from", " ", (0, t.jsx)("span", {
                                className: "text-blue-400",
                                children: e
                            }), ", but the presentation is not controlled by them. Our use of the name", " ", (0, t.jsx)("span", {
                                className: "text-blue-400",
                                children: e
                            }), " is for context, not claiming any ownership. It remains the property of the copyright holder."]
                        })
                    }), (0, t.jsx)("div", {
                        className: "border-t border-zinc-200 dark:border-zinc-800"
                    }), (0, t.jsxs)("div", {
                        className: "flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0",
                        children: [(0, t.jsxs)("div", {
                            className: "flex items-center md:flex-row flex-col gap-3",
                            children: [(0, t.jsx)(r.default, {
                                className: "text-zinc-500 dark:text-zinc-300 hover:text-blue-400 transition-colors duration-200 text-sm font-medium",
                                href: "/terms-of-service",
                                passHref: true,
                                children: "Terms of Service"
                            }), (0, t.jsx)("div", {
                                className: "w-1 h-1 bg-gray-600 rounded-full md:block hidden"
                            }), (0, t.jsx)(r.default, {
                                className: "text-zinc-500 dark:text-zinc-300 hover:text-blue-400 transition-colors duration-200 text-sm font-medium",
                                href: "/privacy-policy",
                                passHref: true,
                                children: "Privacy Policy"
                            }), (0, t.jsx)("div", {
                                className: "w-1 h-1 bg-gray-600 rounded-full md:block hidden"
                            }), (0, t.jsx)("div", {
                                id: "ccpa-link",
                                className: "dark:text-white  dark:bg-black text-zinc-500 text-center text-sm",
                                children: (0, t.jsx)("span", {
                                    "data-ccpa-link": "1"
                                })
                            }), (0, t.jsx)(n, {})]
                        }), (0, t.jsxs)("p", {
                            className: "text-zinc-500 dark:text-zinc-300 text-sm",
                            children: ["© ", (new Date).getFullYear(), " ", (0, t.jsx)("span", {
                                className: "text-zinc-500 dark:text-zinc-300 font-semibold",
                                children: "Livecounts.io"
                            })]
                        })]
                    })]
                })
            })
        });
    }], 7293);
}, 50499, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = [],
        o = "f06e",
        n = "M572.52 241.4C518.29 135.59 410.93 64 288 64S57.68 135.64 3.48 241.41a32.35 32.35 0 0 0 0 29.19C57.71 376.41 165.07 448 288 448s230.32-71.64 284.52-177.41a32.35 32.35 0 0 0 0-29.19zM288 400a144 144 0 1 1 144-144 143.93 143.93 0 0 1-144 144zm0-240a95.31 95.31 0 0 0-25.31 3.79 47.85 47.85 0 0 1-66.9 66.9A95.78 95.78 0 1 0 288 160z";
    r.definition = {
        prefix: "fas",
        iconName: "eye",
        icon: [576, 512, i, o, n]
    }, r.faEye = r.definition, r.prefix = "fas", r.iconName = "eye", r.width = 576, r.height = 512, r.ligatures = i, r.unicode = o, r.svgPathData = n;
}, 66318, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "video",
        o = [],
        n = "f03d",
        s = "M336.2 64H47.8C21.4 64 0 85.4 0 111.8v288.4C0 426.6 21.4 448 47.8 448h288.4c26.4 0 47.8-21.4 47.8-47.8V111.8c0-26.4-21.4-47.8-47.8-47.8zm189.4 37.7L416 177.3v157.4l109.6 75.5c21.2 14.6 50.4-.3 50.4-25.8V127.5c0-25.4-29.1-40.4-50.4-25.8z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [576, 512, o, n, s]
    }, r.faVideo = r.definition, r.prefix = "fas", r.iconName = i, r.width = 576, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 82317, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "bullseye",
        o = [],
        n = "f140",
        s = "M248 8C111.03 8 0 119.03 0 256s111.03 248 248 248 248-111.03 248-248S384.97 8 248 8zm0 432c-101.69 0-184-82.29-184-184 0-101.69 82.29-184 184-184 101.69 0 184 82.29 184 184 0 101.69-82.29 184-184 184zm0-312c-70.69 0-128 57.31-128 128s57.31 128 128 128 128-57.31 128-128-57.31-128-128-128zm0 192c-35.29 0-64-28.71-64-64s28.71-64 64-64 64 28.71 64 64-28.71 64-64 64z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [496, 512, o, n, s]
    }, r.faBullseye = r.definition, r.prefix = "fas", r.iconName = i, r.width = 496, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 50480, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "thumbs-up",
        o = [],
        n = "f164",
        s = "M104 224H24c-13.255 0-24 10.745-24 24v240c0 13.255 10.745 24 24 24h80c13.255 0 24-10.745 24-24V248c0-13.255-10.745-24-24-24zM64 472c-13.255 0-24-10.745-24-24s10.745-24 24-24 24 10.745 24 24-10.745 24-24 24zM384 81.452c0 42.416-25.97 66.208-33.277 94.548h101.723c33.397 0 59.397 27.746 59.553 58.098.084 17.938-7.546 37.249-19.439 49.197l-.11.11c9.836 23.337 8.237 56.037-9.308 79.469 8.681 25.895-.069 57.704-16.382 74.757 4.298 17.598 2.244 32.575-6.148 44.632C440.202 511.587 389.616 512 346.839 512l-2.845-.001c-48.287-.017-87.806-17.598-119.56-31.725-15.957-7.099-36.821-15.887-52.651-16.178-6.54-.12-11.783-5.457-11.783-11.998v-213.77c0-3.2 1.282-6.271 3.558-8.521 39.614-39.144 56.648-80.587 89.117-113.111 14.804-14.832 20.188-37.236 25.393-58.902C282.515 39.293 291.817 0 312 0c24 0 72 8 72 81.452z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [512, 512, o, n, s]
    }, r.faThumbsUp = r.definition, r.prefix = "fas", r.iconName = i, r.width = 512, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 92088, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "thumbs-down",
        o = [],
        n = "f165",
        s = "M0 56v240c0 13.255 10.745 24 24 24h80c13.255 0 24-10.745 24-24V56c0-13.255-10.745-24-24-24H24C10.745 32 0 42.745 0 56zm40 200c0-13.255 10.745-24 24-24s24 10.745 24 24-10.745 24-24 24-24-10.745-24-24zm272 256c-20.183 0-29.485-39.293-33.931-57.795-5.206-21.666-10.589-44.07-25.393-58.902-32.469-32.524-49.503-73.967-89.117-113.111a11.98 11.98 0 0 1-3.558-8.521V59.901c0-6.541 5.243-11.878 11.783-11.998 15.831-.29 36.694-9.079 52.651-16.178C256.189 17.598 295.709.017 343.995 0h2.844c42.777 0 93.363.413 113.774 29.737 8.392 12.057 10.446 27.034 6.148 44.632 16.312 17.053 25.063 48.863 16.382 74.757 17.544 23.432 19.143 56.132 9.308 79.469l.11.11c11.893 11.949 19.523 31.259 19.439 49.197-.156 30.352-26.157 58.098-59.553 58.098H350.723C358.03 364.34 384 388.132 384 430.548 384 504 336 512 312 512z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [512, 512, o, n, s]
    }, r.faThumbsDown = r.definition, r.prefix = "fas", r.iconName = i, r.width = 512, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 68327, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "comment",
        o = [],
        n = "f075",
        s = "M256 32C114.6 32 0 125.1 0 240c0 49.6 21.4 95 57 130.7C44.5 421.1 2.7 466 2.2 466.5c-2.2 2.3-2.8 5.7-1.5 8.7S4.8 480 8 480c66.3 0 116-31.8 140.6-51.4 32.7 12.3 69 19.4 107.4 19.4 141.4 0 256-93.1 256-208S397.4 32 256 32z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [512, 512, o, n, s]
    }, r.faComment = r.definition, r.prefix = "fas", r.iconName = i, r.width = 512, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 39401, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "heart",
        o = [],
        n = "f004",
        s = "M462.3 62.6C407.5 15.9 326 24.3 275.7 76.2L256 96.5l-19.7-20.3C186.1 24.3 104.5 15.9 49.7 62.6c-62.8 53.6-66.1 149.8-9.9 207.9l193.5 199.8c12.5 12.9 32.8 12.9 45.3 0l193.5-199.8c56.3-58.1 53-154.3-9.8-207.9z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [512, 512, o, n, s]
    }, r.faHeart = r.definition, r.prefix = "fas", r.iconName = i, r.width = 512, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 71238, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "user-friends",
        o = [],
        n = "f500",
        s = "M192 256c61.9 0 112-50.1 112-112S253.9 32 192 32 80 82.1 80 144s50.1 112 112 112zm76.8 32h-8.3c-20.8 10-43.9 16-68.5 16s-47.6-6-68.5-16h-8.3C51.6 288 0 339.6 0 403.2V432c0 26.5 21.5 48 48 48h288c26.5 0 48-21.5 48-48v-28.8c0-63.6-51.6-115.2-115.2-115.2zM480 256c53 0 96-43 96-96s-43-96-96-96-96 43-96 96 43 96 96 96zm48 32h-3.8c-13.9 4.8-28.6 8-44.2 8s-30.3-3.2-44.2-8H432c-20.4 0-39.2 5.9-55.7 15.4 24.4 26.3 39.7 61.2 39.7 99.8v38.4c0 2.2-.5 4.3-.6 6.4H592c26.5 0 48-21.5 48-48 0-61.9-50.1-112-112-112z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [640, 512, o, n, s]
    }, r.faUserFriends = r.definition, r.prefix = "fas", r.iconName = i, r.width = 640, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 21357, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "share",
        o = [],
        n = "f064",
        s = "M503.691 189.836L327.687 37.851C312.281 24.546 288 35.347 288 56.015v80.053C127.371 137.907 0 170.1 0 322.326c0 61.441 39.581 122.309 83.333 154.132 13.653 9.931 33.111-2.533 28.077-18.631C66.066 312.814 132.917 274.316 288 272.085V360c0 20.7 24.3 31.453 39.687 18.164l176.004-152c11.071-9.562 11.086-26.753 0-36.328z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [512, 512, o, n, s]
    }, r.faShare = r.definition, r.prefix = "fas", r.iconName = i, r.width = 512, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 36649, (e, t, r) => {
    "use strict";
    Object.defineProperty(r, "__esModule", {
        value: true
    });
    var i = "image",
        o = [],
        n = "f03e",
        s = "M464 448H48c-26.51 0-48-21.49-48-48V112c0-26.51 21.49-48 48-48h416c26.51 0 48 21.49 48 48v288c0 26.51-21.49 48-48 48zM112 120c-30.928 0-56 25.072-56 56s25.072 56 56 56 56-25.072 56-56-25.072-56-56-56zM64 384h384V272l-87.515-87.515c-4.686-4.686-12.284-4.686-16.971 0L208 320l-55.515-55.515c-4.686-4.686-12.284-4.686-16.971 0L64 336v48z";
    r.definition = {
        prefix: "fas",
        iconName: i,
        icon: [512, 512, o, n, s]
    }, r.faImage = r.definition, r.prefix = "fas", r.iconName = i, r.width = 512, r.height = 512, r.ligatures = o, r.unicode = n, r.svgPathData = s;
}, 80830, (e, t, r) => {
    let {
        faEye: i
    } = e.r(50499), {
        faVideo: o
    } = e.r(66318), {
        faBullseye: n
    } = e.r(82317), {
        faThumbsUp: s
    } = e.r(50480), {
        faThumbsDown: a
    } = e.r(92088), {
        faComment: c
    } = e.r(68327), {
        faHeart: d
    } = e.r(39401), {
        faUserFriends: l
    } = e.r(71238), {
        faShare: f
    } = e.r(21357), {
        faImage: u
    } = e.r(36649), {
        faChartBar: h
    } = e.r(94425);
    t.exports = {
        "youtube-live-subscriber-counter": {
            name: "YouTube",
            fullName: "YouTube Live Subscriber Counter",
            icon: "youtube.svg",
            stat: {
                name: "Subscribers",
                icon: l
            },
            search: {
                placeholder: "Search Query / Channel URL / Username..."
            },
            showId: false,
            loadOnClientSide: false,
            refreshTime: 5,
            preferUserId: false,
            colors: {
                theme: "border-red-600 dark:border-red-700",
                graph: "rgb(220, 38, 38)"
            },
            promote: {
                title: "YouTube Channel Promotion",
                priceTier: "high"
            },
            bottomOdos: [
                ["Channel Views", i, "text-blue-500 dark:text-blue-600"],
                ["Videos", o, "text-yellow-500 dark:text-yellow-600"],
                ["Goal", n, "text-red-500 dark:text-red-600"]
            ],
            external: "https://www.youtube.com/channel/"
        },
        "youtube-live-view-counter": {
            name: "YouTube",
            fullName: "YouTube Live View Counter",
            icon: "youtube.svg",
            stat: {
                name: "Views",
                icon: i
            },
            search: {
                placeholder: "Search Query / Video URL / Title..."
            },
            showId: false,
            loadOnClientSide: false,
            refreshTime: 3,
            preferUserId: false,
            colors: {
                theme: "border-red-600 dark:border-red-700",
                graph: "rgb(220, 38, 38)"
            },
            promote: {
                title: "YouTube Video Promotion",
                priceTier: "high"
            },
            bottomOdos: [
                ["Likes", s, "text-green-500 dark:text-green-600"],
                ["Dislikes", a, "text-red-500 dark:text-red-600"],
                ["Comments", c, "text-blue-500 dark:text-blue-600"]
            ],
            external: "https://www.youtube.com/watch?v="
        },
        "tiktok-live-follower-counter": {
            name: "TikTok",
            fullName: "TikTok Live Follower Counter",
            icon: "tiktok.svg",
            stat: {
                name: "Followers",
                icon: l
            },
            search: {
                placeholder: "Search Accounts"
            },
            showId: true,
            loadOnClientSide: false,
            refreshTime: 5,
            preferUserId: true,
            colors: {
                theme: "border-pink-600 dark:border-pink-700",
                graph: "rgb(219, 39, 119)"
            },
            promote: {
                title: "TikTok Account Promotion",
                priceTier: "high"
            },
            bottomOdos: [
                ["Likes", d, "text-red-500 dark:text-red-600"],
                ["Following", l, "text-blue-500 dark:text-blue-600"],
                ["Videos", o, "text-yellow-500 dark:text-yellow-600"]
            ],
            external: "https://www.tiktok.com/@"
        },
        "tiktok-live-view-counter": {
            name: "TikTok",
            fullName: "TikTok Video Live View Counter",
            icon: "tiktok.svg",
            stat: {
                name: "Views",
                icon: i
            },
            search: {
                placeholder: "Video's URL"
            },
            showId: false,
            loadOnClientSide: false,
            refreshTime: 5,
            preferUserId: false,
            colors: {
                theme: "border-pink-600 dark:border-pink-800",
                graph: "rgb(219, 39, 119)"
            },
            promote: {
                title: "TikTok Video Promotion",
                priceTier: "low"
            },
            bottomOdos: [
                ["Likes", d, "text-red-500 dark:text-red-600"],
                ["Comments", c, "text-blue-500 dark:text-blue-600"],
                ["Shares", f, "text-green-500 dark:text-green-600"]
            ],
            external: "https://tiktok.com/@"
        },
        "twitter-live-follower-counter": {
            name: "Twitter/X",
            fullName: "Twitter/X Live Follower Counter",
            icon: "X_icon.png",
            stat: {
                name: "Followers",
                icon: l
            },
            search: {
                placeholder: "@username..."
            },
            showId: true,
            loadOnClientSide: false,
            refreshTime: 30,
            preferUserId: false,
            colors: {
                theme: "border-blue-500 dark:border-blue-800",
                graph: "rgb(59, 130, 246)"
            },
            promote: {
                title: "Twitter Account Promotion",
                priceTier: "low"
            },
            bottomOdos: [
                ["Tweets", c, "text-blue-500 dark:text-blue-400"],
                ["Following", l, "text-green-500 dark:text-green-600"],
                ["Goal", n, "text-red-500 dark:text-red-600"]
            ],
            external: "https://x.com/"
        },
        "twitch-live-follower-counter": {
            name: "Twitch",
            fullName: "Twitch Live Follower Counter",
            icon: "twitch.svg",
            stat: {
                name: "Followers",
                icon: l
            },
            search: {
                placeholder: "Search Query / Channel URL / Username..."
            },
            showId: true,
            loadOnClientSide: true,
            refreshTime: 10,
            preferUserId: true,
            colors: {
                theme: "border-purple-700 dark:border-purple-800",
                graph: "rgb(109, 40, 217)"
            },
            promote: {
                title: "Twitch Account Promotion",
                priceTier: "low"
            },
            bottomOdos: [],
            external: "https://www.twitch.tv/"
        },
        "kick-live-follower-counter": {
            name: "Kick",
            fullName: "Kick Live Follower Counter",
            icon: "kick.png",
            refreshTime: 5,
            stat: {
                name: "Followers",
                icon: l
            },
            search: {
                placeholder: "Username..."
            },
            showId: true,
            loadOnClientSide: true,
            preferUserId: false,
            colors: {
                theme: "border-green-300 dark:border-green-600",
                graph: "#1DB954"
            },
            promote: {
                title: "Kick Channel Promotion",
                priceTier: "low"
            },
            bottomOdos: [
                ["Viewers Live", i, "text-green-500 dark:text-green-600"]
            ],
            external: "https://kick.com/"
        }
    };
}, 53312, e => {
    "use strict";
    var t = e.i(91788);
    class r extends t.Component {
        render() {
            let {
                type: e
            } = this.props;
            return null;
        }
    }
    e.s(["default", () => r]);
}, 38980, e => {
    "use strict";
    var t = e.i(91398);
    e.s(["default", 0, function({
        children: e,
        className: r
    }) {
        return (0, t.jsx)("div", {
            className: `text-white rounded-md shadow-lg ${r && r || ""}`,
            children: e
        });
    }]);
}, 74580, (e, t, r) => {
    t.exports = e => {
        let t = Math.floor(Math.log10(e));
        return Math.ceil(e / 10 ** t) * 10 ** t - e;
    };
}, 25026, (e, t, r) => {
    ! function(i, o) {
        if ("object" == typeof r) t.exports = r = o();
        else if ("function" == typeof define && define.amd) {
            let t;
            undefined !== (t = o()) && e.v(t);
        } else i.CryptoJS = o();
    }(e.e, function() {
        var t = t || function(t, r) {
            if ("undefined" != typeof window && window.crypto && (i = window.crypto), "undefined" != typeof self && self.crypto && (i = self.crypto), "undefined" != typeof globalThis && globalThis.crypto && (i = globalThis.crypto), !i && "undefined" != typeof window && window.msCrypto && (i = window.msCrypto), !i && e.g.crypto && (i = e.g.crypto), !i) try {
                i = {};
            } catch (e) {}
            var i, o = function() {
                    if (i) {
                        if ("function" == typeof i.getRandomValues) try {
                            return i.getRandomValues(new Uint32Array(1))[0];
                        } catch (e) {}
                        if ("function" == typeof i.randomBytes) try {
                            return i.randomBytes(4).readInt32LE();
                        } catch (e) {}
                    }
                    throw Error("Native crypto module could not be used to get secure random number.");
                },
                n = Object.create || function() {
                    function e() {}
                    return function(t) {
                        var r;
                        return e.prototype = t, r = new e, e.prototype = null, r;
                    };
                }(),
                s = {},
                a = s.lib = {},
                c = a.Base = {
                    extend: function(e) {
                        var t = n(this);
                        return e && t.mixIn(e), t.hasOwnProperty("init") && this.init !== t.init || (t.init = function() {
                            t.$super.init.apply(this, arguments);
                        }), t.init.prototype = t, t.$super = this, t;
                    },
                    create: function() {
                        var e = this.extend();
                        return e.init.apply(e, arguments), e;
                    },
                    init: function() {},
                    mixIn: function(e) {
                        for (var t in e) e.hasOwnProperty(t) && (this[t] = e[t]);
                        e.hasOwnProperty("toString") && (this.toString = e.toString);
                    },
                    clone: function() {
                        return this.init.prototype.extend(this);
                    }
                },
                d = a.WordArray = c.extend({
                    init: function(e, t) {
                        e = this.words = e || [], r != t ? this.sigBytes = t : this.sigBytes = 4 * e.length;
                    },
                    toString: function(e) {
                        return (e || f).stringify(this);
                    },
                    concat: function(e) {
                        var t = this.words,
                            r = e.words,
                            i = this.sigBytes,
                            o = e.sigBytes;
                        if (this.clamp(), i % 4)
                            for (var n = 0; n < o; n++) {
                                var s = r[n >>> 2] >>> 24 - n % 4 * 8 & 255;
                                t[i + n >>> 2] |= s << 24 - (i + n) % 4 * 8;
                            } else
                                for (var a = 0; a < o; a += 4) t[i + a >>> 2] = r[a >>> 2];
                        return this.sigBytes += o, this;
                    },
                    clamp: function() {
                        var e = this.words,
                            r = this.sigBytes;
                        e[r >>> 2] &= 4294967295 << 32 - r % 4 * 8, e.length = t.ceil(r / 4);
                    },
                    clone: function() {
                        var e = c.clone.call(this);
                        return e.words = this.words.slice(0), e;
                    },
                    random: function(e) {
                        for (var t = [], r = 0; r < e; r += 4) t.push(o());
                        return new d.init(t, e);
                    }
                }),
                l = s.enc = {},
                f = l.Hex = {
                    stringify: function(e) {
                        for (var t = e.words, r = e.sigBytes, i = [], o = 0; o < r; o++) {
                            var n = t[o >>> 2] >>> 24 - o % 4 * 8 & 255;
                            i.push((n >>> 4).toString(16)), i.push((15 & n).toString(16));
                        }
                        return i.join("");
                    },
                    parse: function(e) {
                        for (var t = e.length, r = [], i = 0; i < t; i += 2) r[i >>> 3] |= parseInt(e.substr(i, 2), 16) << 24 - i % 8 * 4;
                        return new d.init(r, t / 2);
                    }
                },
                u = l.Latin1 = {
                    stringify: function(e) {
                        for (var t = e.words, r = e.sigBytes, i = [], o = 0; o < r; o++) {
                            var n = t[o >>> 2] >>> 24 - o % 4 * 8 & 255;
                            i.push(String.fromCharCode(n));
                        }
                        return i.join("");
                    },
                    parse: function(e) {
                        for (var t = e.length, r = [], i = 0; i < t; i++) r[i >>> 2] |= (255 & e.charCodeAt(i)) << 24 - i % 4 * 8;
                        return new d.init(r, t);
                    }
                },
                h = l.Utf8 = {
                    stringify: function(e) {
                        try {
                            return decodeURIComponent(escape(u.stringify(e)));
                        } catch (e) {
                            throw Error("Malformed UTF-8 data");
                        }
                    },
                    parse: function(e) {
                        return u.parse(unescape(encodeURIComponent(e)));
                    }
                },
                x = a.BufferedBlockAlgorithm = c.extend({
                    reset: function() {
                        this._data = new d.init, this._nDataBytes = 0;
                    },
                    _append: function(e) {
                        "string" == typeof e && (e = h.parse(e)), this._data.concat(e), this._nDataBytes += e.sigBytes;
                    },
                    _process: function(e) {
                        var r, i = this._data,
                            o = i.words,
                            n = i.sigBytes,
                            s = this.blockSize,
                            a = n / (4 * s),
                            c = (a = e ? t.ceil(a) : t.max((0 | a) - this._minBufferSize, 0)) * s,
                            l = t.min(4 * c, n);
                        if (c) {
                            for (var f = 0; f < c; f += s) this._doProcessBlock(o, f);
                            r = o.splice(0, c), i.sigBytes -= l;
                        }
                        return new d.init(r, l);
                    },
                    clone: function() {
                        var e = c.clone.call(this);
                        return e._data = this._data.clone(), e;
                    },
                    _minBufferSize: 0
                });
            a.Hasher = x.extend({
                cfg: c.extend(),
                init: function(e) {
                    this.cfg = this.cfg.extend(e), this.reset();
                },
                reset: function() {
                    x.reset.call(this), this._doReset();
                },
                update: function(e) {
                    return this._append(e), this._process(), this;
                },
                finalize: function(e) {
                    return e && this._append(e), this._doFinalize();
                },
                blockSize: 16,
                _createHelper: function(e) {
                    return function(t, r) {
                        return new e.init(r).finalize(t);
                    };
                },
                _createHmacHelper: function(e) {
                    return function(t, r) {
                        return new p.HMAC.init(e, r).finalize(t);
                    };
                }
            });
            var p = s.algo = {};
            return s;
        }(Math);
        return t;
    });
}, 16713, (e, t, r) => {
    ! function(i, o) {
        if ("object" == typeof r) t.exports = r = o(e.r(25026));
        else if ("function" == typeof define && define.amd) {
            let t;
            undefined !== (t = o(e.r(25026))) && e.v(t);
        } else o(i.CryptoJS);
    }(e.e, function(e) {
        var t, r, i, o;
        return r = (t = e.lib).Base, i = t.WordArray, (o = e.x64 = {}).Word = r.extend({
            init: function(e, t) {
                this.high = e, this.low = t;
            }
        }), o.WordArray = r.extend({
            init: function(e, t) {
                e = this.words = e || [], undefined != t ? this.sigBytes = t : this.sigBytes = 8 * e.length;
            },
            toX32: function() {
                for (var e = this.words, t = e.length, r = [], o = 0; o < t; o++) {
                    var n = e[o];
                    r.push(n.high), r.push(n.low);
                }
                return i.create(r, this.sigBytes);
            },
            clone: function() {
                for (var e = r.clone.call(this), t = e.words = this.words.slice(0), i = t.length, o = 0; o < i; o++) t[o] = t[o].clone();
                return e;
            }
        }), e;
    });
}, 66528, (e, t, r) => {
    ! function(i, o, n) {
        if ("object" == typeof r) t.exports = r = o(e.r(25026), e.r(16713));
        else if ("function" == typeof define && define.amd) {
            let t;
            undefined !== (t = o(e.r(25026), e.r(16713))) && e.v(t);
        } else o(i.CryptoJS);
    }(e.e, function(e) {
        return ! function() {
            var t = e.lib.Hasher,
                r = e.x64,
                i = r.Word,
                o = r.WordArray,
                n = e.algo;
            for (var a = [i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments), i.create.apply(i, arguments)], c = [], d = 0; d < 80; d++) c[d] = i.create.apply(i, arguments);
            var l = n.SHA512 = t.extend({
                _doReset: function() {
                    this._hash = new o.init([new i.init(1779033703, 4089235720), new i.init(3144134277, 2227873595), new i.init(1013904242, 4271175723), new i.init(2773480762, 1595750129), new i.init(1359893119, 2917565137), new i.init(2600822924, 725511199), new i.init(528734635, 4215389547), new i.init(1541459225, 327033209)]);
                },
                _doProcessBlock: function(e, t) {
                    for (var r = this._hash.words, i = r[0], o = r[1], n = r[2], s = r[3], d = r[4], l = r[5], f = r[6], u = r[7], h = i.high, x = i.low, p = o.high, b = o.low, w = n.high, m = n.low, v = s.high, g = s.low, y = d.high, k = d.low, _ = l.high, C = l.low, j = f.high, z = f.low, S = u.high, T = u.low, H = h, N = x, P = p, B = b, M = w, A = m, I = v, O = g, U = y, D = k, R = _, V = C, $ = j, L = z, F = S, W = T, E = 0; E < 80; E++) {
                        var J, Y, K = c[E];
                        if (E < 16) Y = K.high = 0 | e[t + 2 * E], J = K.low = 0 | e[t + 2 * E + 1];
                        else {
                            var X = c[E - 15],
                                q = X.high,
                                Q = X.low,
                                G = (q >>> 1 | Q << 31) ^ (q >>> 8 | Q << 24) ^ q >>> 7,
                                Z = (Q >>> 1 | q << 31) ^ (Q >>> 8 | q << 24) ^ (Q >>> 7 | q << 25),
                                ee = c[E - 2],
                                et = ee.high,
                                er = ee.low,
                                ei = (et >>> 19 | er << 13) ^ (et << 3 | er >>> 29) ^ et >>> 6,
                                eo = (er >>> 19 | et << 13) ^ (er << 3 | et >>> 29) ^ (er >>> 6 | et << 26),
                                en = c[E - 7],
                                es = en.high,
                                ea = en.low,
                                ec = c[E - 16],
                                ed = ec.high,
                                el = ec.low;
                            Y = G + es + +((J = Z + ea) >>> 0 < Z >>> 0), J += eo, Y = Y + ei + +(J >>> 0 < eo >>> 0), J += el, K.high = Y = Y + ed + +(J >>> 0 < el >>> 0), K.low = J;
                        }
                        var ef = U & R ^ ~U & $,
                            eu = D & V ^ ~D & L,
                            eh = H & P ^ H & M ^ P & M,
                            ex = N & B ^ N & A ^ B & A,
                            ep = (H >>> 28 | N << 4) ^ (H << 30 | N >>> 2) ^ (H << 25 | N >>> 7),
                            eb = (N >>> 28 | H << 4) ^ (N << 30 | H >>> 2) ^ (N << 25 | H >>> 7),
                            ew = (U >>> 14 | D << 18) ^ (U >>> 18 | D << 14) ^ (U << 23 | D >>> 9),
                            em = (D >>> 14 | U << 18) ^ (D >>> 18 | U << 14) ^ (D << 23 | U >>> 9),
                            ev = a[E],
                            eg = ev.high,
                            ey = ev.low,
                            ek = W + em,
                            e_ = F + ew + +(ek >>> 0 < W >>> 0),
                            ek = ek + eu,
                            e_ = e_ + ef + +(ek >>> 0 < eu >>> 0),
                            ek = ek + ey,
                            e_ = e_ + eg + +(ek >>> 0 < ey >>> 0),
                            ek = ek + J,
                            e_ = e_ + Y + +(ek >>> 0 < J >>> 0),
                            eC = eb + ex,
                            ej = ep + eh + +(eC >>> 0 < eb >>> 0);
                        F = $, W = L, $ = R, L = V, R = U, V = D, U = I + e_ + +((D = O + ek | 0) >>> 0 < O >>> 0) | 0, I = M, O = A, M = P, A = B, P = H, B = N, H = e_ + ej + +((N = ek + eC | 0) >>> 0 < ek >>> 0) | 0;
                    }
                    x = i.low = x + N, i.high = h + H + +(x >>> 0 < N >>> 0), b = o.low = b + B, o.high = p + P + +(b >>> 0 < B >>> 0), m = n.low = m + A, n.high = w + M + +(m >>> 0 < A >>> 0), g = s.low = g + O, s.high = v + I + +(g >>> 0 < O >>> 0), k = d.low = k + D, d.high = y + U + +(k >>> 0 < D >>> 0), C = l.low = C + V, l.high = _ + R + +(C >>> 0 < V >>> 0), z = f.low = z + L, f.high = j + $ + +(z >>> 0 < L >>> 0), T = u.low = T + W, u.high = S + F + +(T >>> 0 < W >>> 0);
                },
                _doFinalize: function() {
                    var e = this._data,
                        t = e.words,
                        r = 8 * this._nDataBytes,
                        i = 8 * e.sigBytes;
                    return t[i >>> 5] |= 128 << 24 - i % 32, t[(i + 128 >>> 10 << 5) + 30] = Math.floor(r / 4294967296), t[(i + 128 >>> 10 << 5) + 31] = r, e.sigBytes = 4 * t.length, this._process(), this._hash.toX32();
                },
                clone: function() {
                    var e = t.clone.call(this);
                    return e._hash = this._hash.clone(), e;
                },
                blockSize: 32
            });
            e.SHA512 = t._createHelper(l), e.HmacSHA512 = t._createHmacHelper(l);
        }(), e.SHA512;
    });
}, 90642, (e, t, r) => {
    ! function(i, o, n) {
        if ("object" == typeof r) t.exports = r = o(e.r(25026), e.r(16713), e.r(66528));
        else if ("function" == typeof define && define.amd) {
            let t;
            undefined !== (t = o(e.r(25026), e.r(16713), e.r(66528))) && e.v(t);
        } else o(i.CryptoJS);
    }(e.e, function(e) {
        var t, r, i, o, n, s;
        return r = (t = e.x64).Word, i = t.WordArray, n = (o = e.algo).SHA512, s = o.SHA384 = n.extend({
            _doReset: function() {
                this._hash = new i.init([new r.init(3418070365, 3238371032), new r.init(1654270250, 914150663), new r.init(2438529370, 812702999), new r.init(355462360, 4144912697), new r.init(1731405415, 4290775857), new r.init(2394180231, 1750603025), new r.init(3675008525, 1694076839), new r.init(1203062813, 3204075428)]);
            },
            _doFinalize: function() {
                var e = n._doFinalize.call(this);
                return e.sigBytes -= 16, e;
            }
        }), e.SHA384 = n._createHelper(s), e.HmacSHA384 = n._createHmacHelper(s), e.SHA384;
    });
}, 35521, (e, t, r) => {
    ! function(i, o) {
        if ("object" == typeof r) t.exports = r = o(e.r(25026));
        else if ("function" == typeof define && define.amd) {
            let t;
            undefined !== (t = o(e.r(25026))) && e.v(t);
        } else o(i.CryptoJS);
    }(e.e, function(e) {
        return ! function(t) {
            var r = e.lib,
                i = r.WordArray,
                o = r.Hasher,
                n = e.algo,
                s = [],
                a = [];
            for (var d = 2, l = 0; l < 64;)(function(e) {
                for (var r = t.sqrt(e), i = 2; i <= r; i++)
                    if (!(e % i)) return false;
                return true;
            }(d) && (l < 8 && (s[l] = (t.pow(d, 0.5) - (0 | t.pow(d, 0.5))) * 4294967296 | 0), a[l] = (t.pow(d, 0.3333333333333333) - (0 | t.pow(d, 0.3333333333333333))) * 4294967296 | 0, l++), d++);
            var f = [],
                u = n.SHA256 = o.extend({
                    _doReset: function() {
                        this._hash = new i.init(s.slice(0));
                    },
                    _doProcessBlock: function(e, t) {
                        for (var r = this._hash.words, i = r[0], o = r[1], n = r[2], s = r[3], c = r[4], d = r[5], l = r[6], u = r[7], h = 0; h < 64; h++) {
                            if (h < 16) f[h] = 0 | e[t + h];
                            else {
                                var x = f[h - 15],
                                    p = (x << 25 | x >>> 7) ^ (x << 14 | x >>> 18) ^ x >>> 3,
                                    b = f[h - 2],
                                    w = (b << 15 | b >>> 17) ^ (b << 13 | b >>> 19) ^ b >>> 10;
                                f[h] = p + f[h - 7] + w + f[h - 16];
                            }
                            var m = c & d ^ ~c & l,
                                v = i & o ^ i & n ^ o & n,
                                g = (i << 30 | i >>> 2) ^ (i << 19 | i >>> 13) ^ (i << 10 | i >>> 22),
                                y = u + ((c << 26 | c >>> 6) ^ (c << 21 | c >>> 11) ^ (c << 7 | c >>> 25)) + m + a[h] + f[h],
                                k = g + v;
                            u = l, l = d, d = c, c = s + y | 0, s = n, n = o, o = i, i = y + k | 0;
                        }
                        r[0] = r[0] + i | 0, r[1] = r[1] + o | 0, r[2] = r[2] + n | 0, r[3] = r[3] + s | 0, r[4] = r[4] + c | 0, r[5] = r[5] + d | 0, r[6] = r[6] + l | 0, r[7] = r[7] + u | 0;
                    },
                    _doFinalize: function() {
                        var e = this._data,
                            r = e.words,
                            i = 8 * this._nDataBytes,
                            o = 8 * e.sigBytes;
                        return r[o >>> 5] |= 128 << 24 - o % 32, r[(o + 64 >>> 9 << 4) + 14] = t.floor(i / 4294967296), r[(o + 64 >>> 9 << 4) + 15] = i, e.sigBytes = 4 * r.length, this._process(), this._hash;
                    },
                    clone: function() {
                        var e = o.clone.call(this);
                        return e._hash = this._hash.clone(), e;
                    }
                });
            e.SHA256 = o._createHelper(u), e.HmacSHA256 = o._createHmacHelper(u);
        }(Math), e.SHA256;
    });
}, 88114, (e, t, r) => {
    ! function(i, o) {
        if ("object" == typeof r) t.exports = r = o(e.r(25026));
        else if ("function" == typeof define && define.amd) {
            let t;
            undefined !== (t = o(e.r(25026))) && e.v(t);
        } else o(i.CryptoJS);
    }(e.e, function(e) {
        return ! function(t) {
            var r = e.lib,
                i = r.WordArray,
                o = r.Hasher,
                n = e.algo,
                s = i.create([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8, 3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12, 1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2, 4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]),
                a = i.create([5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12, 6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2, 15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13, 8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14, 12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]),
                c = i.create([11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8, 7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12, 11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5, 11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12, 9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]),
                d = i.create([8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6, 9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11, 9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5, 15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8, 8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]),
                l = i.create([0, 1518500249, 1859775393, 2400959708, 2840853838]),
                f = i.create([1352829926, 1548603684, 1836072691, 2053994217, 0]),
                u = n.RIPEMD160 = o.extend({
                    _doReset: function() {
                        this._hash = i.create([1732584193, 4023233417, 2562383102, 271733878, 3285377520]);
                    },
                    _doProcessBlock: function(e, t) {
                        for (var r, i, o, n, u, x, p, b, w, m, v, g, y, k, _, C, j, z, S, T = 0; T < 16; T++) {
                            var H = t + T,
                                N = e[H];
                            e[H] = (N << 8 | N >>> 24) & 16711935 | (N << 24 | N >>> 8) & 4278255360;
                        }
                        var P = this._hash.words,
                            B = l.words,
                            M = f.words,
                            A = s.words,
                            I = a.words,
                            O = c.words,
                            U = d.words;
                        k = w = P[0], _ = m = P[1], C = v = P[2], j = g = P[3], z = y = P[4];
                        for (var T = 0; T < 80; T += 1) {
                            S = w + e[t + A[T]] | 0, T < 16 ? S += (m ^ v ^ g) + B[0] : T < 32 ? S += ((r = m) & v | ~r & g) + B[1] : T < 48 ? S += ((m | ~v) ^ g) + B[2] : T < 64 ? S += (i = m, o = v, (i & (n = g) | o & ~n) + B[3]) : S += (m ^ (v | ~g)) + B[4], S |= 0, S = (S = S << O[T] | S >>> 32 - O[T]) + y | 0, w = y, y = g, g = v << 10 | v >>> 22, v = m, m = S, S = k + e[t + I[T]] | 0, T < 16 ? S += (_ ^ (C | ~j)) + M[0] : T < 32 ? S += (u = _, x = C, (u & (p = j) | x & ~p) + M[1]) : T < 48 ? S += ((_ | ~C) ^ j) + M[2] : T < 64 ? S += ((b = _) & C | ~b & j) + M[3] : S += (_ ^ C ^ j) + M[4], S |= 0, S = (S = S << U[T] | S >>> 32 - U[T]) + z | 0, k = z, z = j, j = C << 10 | C >>> 22, C = _, _ = S;
                        }
                        S = P[1] + v + j | 0, P[1] = P[2] + g + z | 0, P[2] = P[3] + y + k | 0, P[3] = P[4] + w + _ | 0, P[4] = P[0] + m + C | 0, P[0] = S;
                    },
                    _doFinalize: function() {
                        var e = this._data,
                            t = e.words,
                            r = 8 * this._nDataBytes,
                            i = 8 * e.sigBytes;
                        t[i >>> 5] |= 128 << 24 - i % 32, t[(i + 64 >>> 9 << 4) + 14] = (r << 8 | r >>> 24) & 16711935 | (r << 24 | r >>> 8) & 4278255360, e.sigBytes = (t.length + 1) * 4, this._process();
                        for (var o = this._hash, n = o.words, s = 0; s < 5; s++) {
                            var a = n[s];
                            n[s] = (a << 8 | a >>> 24) & 16711935 | (a << 24 | a >>> 8) & 4278255360;
                        }
                        return o;
                    },
                    clone: function() {
                        var e = o.clone.call(this);
                        return e._hash = this._hash.clone(), e;
                    }
                });
            e.RIPEMD160 = o._createHelper(u), e.HmacRIPEMD160 = o._createHmacHelper(u);
        }(Math), e.RIPEMD160;
    });
}, 90165, (e, t, r) => {
    let i = e.r(90642), // this is SHA384
        o = e.r(35521), // this is SHA256
        n = e.r(88114); // this is RIPEMD160
    t.exports = () => {
        let e = Date.now().toString();
        return {
            "x-midas": i(o(e + 64)),
            "x-ajay": n(e),
            "x-catto": e
        };
    };
}, 46542, (e, t, r) => {
    "use strict";
    var i = "undefined" != typeof self ? self : "undefined" != typeof window ? window : e.g;
    t.exports = r = i.fetch, i.fetch && (r.default = i.fetch.bind(i)), r.Headers = i.Headers, r.Request = i.Request, r.Response = i.Response;
}, 78406, (e, t, r) => {
    let i = e.r(90165);
    t.exports = async (e, t, r, o) => {
        switch (!o && (o = {}), t) {
            case "stats":
                try {
                    let e = await fetch(`https://tiktok.livecounts.io/user/stats/${r}`, {
                        headers: {
                            ...i()
                        }
                    }).then(e => e.json());
                    if (!e.success) return {
                        success: false
                    };
                    return {
                        success: true,
                        followerCount: e.followerCount,
                        bottomOdos: [e.likeCount, e.followingCount, e.videoCount]
                    };
                } catch (e) {
                    return {
                        success: false
                    };
                }
            case "search":
                try {
                    let e = await fetch(`https://tiktok.livecounts.io/user/search/${encodeURIComponent(r)}`, {
                        headers: {
                            ...i()
                        }
                    }).then(e => e.json());
                    if (!e.success) return {
                        success: false
                    };
                    return {
                        success: true,
                        userData: e.userData
                    };
                } catch (e) {
                    return console.log(e.message), {
                        success: false
                    };
                }
            case "data":
                try {
                    let e = await fetch(`https://tiktok.livecounts.io/user/data/${r}`, {
                        headers: {
                            "User-Agent": "+https://github.com/bitinn/node-fetch",
                            "x-antiabuse-ip": o["cf-connecting-ip"],
                            "x-user-agent": o["user-agent"],
                            "x-ray-id": o["cf-ray"],
                            "x-service": "Livecounts.io"
                        }
                    }).then(e => e.json());
                    return console.log(e), {
                        banner: e.avatar,
                        name: e.username,
                        ...e
                    };
                } catch (e) {
                    return console.log(e), {
                        success: false
                    };
                }
        }
    };
}, 27681, (e, t, r) => {
    let i = e.r(90165);
    e.r(74580), t.exports = async (e, t, r) => {
        switch (t) {
            case "search":
                return {
                    success: true, userData: (await fetch(`https://api.livecounts.io/twitch-live-follower-counter/search/${encodeURIComponent(r)}`, {
                        headers: {
                            ...i()
                        }
                    }).then(e => e.json())).userData
                };
            case "stats":
                return {
                    ...await fetch(`https://api.livecounts.io/twitch-live-follower-counter/stats/${r}`, {
                        headers: {
                            ...i()
                        }
                    }).then(e => e.json())
                };
            case "data":
                return await fetch(`https://api.livecounts.io/twitch-live-follower-counter/data/${r}`, {
                    headers: {
                        "User-Agent": "+https://github.com/bitinn/node-fetch",
                        ...i()
                    }
                }).then(e => e.json());
        }
    };
}, 96654, (e, t, r) => {
    let i = e.r(90165);
    t.exports = async (e, t, r) => {
        switch (t) {
            case "data": {
                let e = await fetch(`https://tiktok.livecounts.io/video/data/${r}`, {
                    headers: {
                        "User-Agent": "+https://github.com/bitinn/node-fetch",
                        ...i()
                    }
                }).then(e => e.json());
                return {
                    success: true,
                    id: r,
                    name: e.title,
                    description: "",
                    avatar: e.cover,
                    banner: e.cover,
                    verified: false
                };
            }
            case "search":
                if (r.includes("vm.tiktok.com")) {
                    let e = await fetch(`https://api.tokcount.com/?type=videoID&username=${encodeURIComponent(r)}`, {
                        headers: {
                            ...i()
                        }
                    }).then(e => e.json());
                    if (!e.id) return;
                    let t = await fetch(`https://tiktok.livecounts.io/video/data/${e.id}`, {
                        headers: i()
                    }).then(e => e.json());
                    return {
                        success: true,
                        userData: [{
                            id: t.id,
                            username: t.title,
                            avatar: t.cover
                        }]
                    };
                } {
                    let e = (r = r.split("?")[0]).split("/")[5];
                    if (19 != e.length) return;
                    let t = await fetch(`https://tiktok.livecounts.io/video/data/${e}`, {
                        headers: i()
                    }).then(e => e.json());
                    return {
                        success: true,
                        userData: [{
                            id: e,
                            username: t.title,
                            avatar: t.cover
                        }]
                    };
                }
            case "stats": {
                let e = await fetch(`https://tiktok.livecounts.io/video/stats/${r}`, {
                    headers: {
                        ...i()
                    }
                }).then(e => e.json());
                return {
                    success: true,
                    followerCount: e.viewCount,
                    bottomOdos: [e.likeCount, e.commentCount, e.shareCount]
                };
            }
        }
    };
}, 64470, (e, t, r) => {
    let i = {};
    t.exports = (e, [t], r) => {
        if (t = parseInt(t), e = parseInt(e), !t) return e;
        let o = e / t;
        i[r] && i[r].views || (i[r] = {
            views: e,
            likes: t,
            estViews: e
        });
        let n = t - i[r].likes;
        if (n < 0) return i[r].estViews;
        let s = e + Math.round(n * o);
        return i[r].views != e && (i[r].views = e, i[r].likes = t), i[r].estViews = s, s;
    };
}, 76393, (e, t, r) => {
    var i;
    let o = e.r(64470),
        n = e.r(90165);
    t.exports = async (e, t, r) => {
        if ("stats" === t) {
            let e = await fetch(`https://api.livecounts.io/youtube-live-view-counter/stats/${r}`, {
                headers: {
                    ...n()
                }
            }).then(e => e.json());
            if (!i) try {
                let t = await fetch(`https://returnyoutubedislikeapi.com/votes?videoId=${r}`).then(e => e.json());
                t.dislikes && e.bottomOdos.splice(1, 1, t.dislikes), setTimeout(() => {
                    i = false;
                }, 18e5), i = true;
            } catch (e) {
                i = true;
            }
            return e.followerCount = o(e.followerCount, e.bottomOdos, r), e;
        } {
            let e = {};
            return "data" == t && (e = {
                "x-from": "tokcount-frontend/1.245543435xdhfg"
            }), JSON.parse(await fetch(`https://api.livecounts.io/youtube-live-view-counter/${t}/${"search" == t ? encodeURIComponent(r) : r}`, {
                headers: {
                    "User-Agent": "+https://github.com/bitinn/node-fetch",
                    ...n(),
                    ...e
                }
            }).then(e => e.text())) || {
                success: false
            };
        }
    };
}, 97630, (e, t, r) => {
    let i = e.r(46542);
    e.r(90165), t.exports = async (e, t, r, o) => {
        switch (t) {
            case "data":
                try {
                    let e = await i(`https://kick.com/api/v1/channels/${r}`, {}).then(e => e.json());
                    return {
                        success: true,
                        id: r,
                        userId: e.user.id,
                        name: e.user.username,
                        description: e.user.bio,
                        avatar: e.user.profile_pic ? e.user.profile_pic : "https://dbxmjjzl5pc1g.cloudfront.net/31fb8812-6dc3-4290-8c21-bd543871b6d5/images/user-profile-pic.png",
                        banner: e.banner ? e.banner_image.url : e.user.profile_pic ? e.user.profile_pic : "https://dbxmjjzl5pc1g.cloudfront.net/31fb8812-6dc3-4290-8c21-bd543871b6d5/images/user-profile-pic.png",
                        verified: e.verified,
                        followerCount: e.followersCount,
                        bottomOdos: [e.livestream ? e.livestream.viewer_count : 0]
                    };
                } catch (e) {
                    return console.log(e), {
                        success: false
                    };
                }
            case "stats":
                try {
                    let e = await i(`https://kick.com/api/v1/channels/${r}`, {}).then(e => e.json());
                    return {
                        success: true,
                        followerCount: e.followersCount,
                        bottomOdos: [e.livestream ? e.livestream.viewer_count : 0]
                    };
                } catch (e) {
                    return {
                        success: false
                    };
                }
            case "search":
                try {
                    let e = await i(`https://kick.com/api/search?searched_word=${encodeURIComponent(r)}`, {}).then(e => e.json()),
                        t = (e && Array.isArray(e.channels) ? e.channels : []).map(e => ({
                            id: e.slug,
                            userId: e.userId,
                            username: e.user && e.user.username ? e.user.username : undefined,
                            avatar: e.user && e.user.profilePic ? e.user.profilePic : "https://dbxmjjzl5pc1g.cloudfront.net/31fb8812-6dc3-4290-8c21-bd543871b6d5/images/user-profile-pic.png",
                            verified: !!e.verified && undefined !== e.verified.id && null !== e.verified.id,
                            is_live: e.isLive,
                            followers_count: e.followers_count
                        }));
                    return {
                        success: true,
                        userData: t
                    };
                } catch (e) {
                    return console.log(e.message), {
                        success: false
                    };
                }
        }
    };
}, 62834, (e, t, r) => {
    let i = e.r(90165),
        o = e.r(46542),
        n = e.r(7090),
        s = e.r(78406),
        a = e.r(27681),
        c = e.r(96654),
        d = e.r(76393),
        l = e.r(97630);
    t.exports = async (e, t, r, f, u) => {
        switch (e) {
            case "tiktok-live-follower-counter":
                return s(e, t, r, f, u);
            case "tiktok-live-view-counter":
                return c(e, t, r);
            case "twitch-live-follower-counter":
                return a(e, t, r);
            case "youtube-live-view-counter":
                return d(e, t, r);
            case "kick-live-follower-counter":
                return l(e, t, r);
            default:
                try {
                    let s = {};
                    return "twitter-live-follower-counter" == e && "data" == t && (s = {
                        "x-from": "tokcount-frontend/1.245543435xdhfg"
                    }), await o(`${n.apiHostname}/${e}/${t}/${t && "search" == t && encodeURIComponent(r) || r}`, {
                        headers: {
                            ...i(),
                            ...s
                        }
                    }).then(e => e.json());
                } catch (e) {
                    return console.log(e), {
                        success: false
                    };
                }
        }
    };
}]);
