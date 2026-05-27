
() => {
    const map = new Map([
        ["appCodeName", "Mozilla"],
        ["appName", "Netscape"],
        ["platform", "iPhone"],
        ["product", "Gecko"],
        ["productSub", "20030107"],
        ["vendor", "Apple Computer, Inc."],
        ["vendorSub", ""],
        ["standalone", false],
        ["cookieEnabled", true],
        ["onLine", true],
        ["webdriver", false],
        ["pdfViewerEnabled", true],
        ["buildID", undefined],
        ["oscpu", undefined],
        ["globalPrivacyControl", undefined],
    ]);
      
    for (const [key, value] of map.entries()) {
        Object.defineProperty(Object.getPrototypeOf(navigator), key, {get: () => value})
    }

    delete Object.getPrototypeOf(navigator).getBattery
    delete Object.getPrototypeOf(navigator).deviceMemory

    const getParameterProxyHandler = {
        apply: function (target, ctx, args) {
            const param = (args || [])[0]
            if ( param === 37445 ) { return "Apple Inc." }
            if ( param === 37446 ) { return "Apple GPU"  }

            return utils.cache.Reflect.apply(target, ctx, args)
        }
    }

    const addProxy = (object, property_name) => {utils.replaceWithProxy(object, property_name, getParameterProxyHandler)}

    addProxy(WebGLRenderingContext.prototype,  "getParameter")
    addProxy(WebGL2RenderingContext.prototype, "getParameter")

    try {
        if (window.outerWidth && window.outerHeight) { return }
        const windowFrame = 500//85
        window.outerWidth = window.innerWidth
        window.outerHeight = window.innerHeight + windowFrame
    } catch (err) {

    }

    // delete Object.getPrototypeOf(navigator).webdriver
}
