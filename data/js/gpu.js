(() => {
    const gpuConfigs = {
        'iPhone SE': {
            vendor: 'Apple Inc.',
            renderer: 'Apple A13 GPU',
            shadingLanguageVersion: 'WebGL GLSL ES 3.00',
            version: 'WebGL 2.0',
            maxVertexAttribs: 16,
            maxTextureSize: 16384,
            maxViewportDims: [16384, 16384]
        },
        'iPhone 11': {
            vendor: 'Apple Inc.',
            renderer: 'Apple A13 GPU',
            shadingLanguageVersion: 'WebGL GLSL ES 3.00',
            version: 'WebGL 2.0',
            maxVertexAttribs: 16,
            maxTextureSize: 16384,
            maxViewportDims: [16384, 16384]
        },
        'iPhone 12': {
            vendor: 'Apple Inc.',
            renderer: 'Apple A14 GPU',
            shadingLanguageVersion: 'WebGL GLSL ES 3.00',
            version: 'WebGL 2.0',
            maxVertexAttribs: 16,
            maxTextureSize: 16384,
            maxViewportDims: [16384, 16384]
        },
        'iPhone 13': {
            vendor: 'Apple Inc.',
            renderer: 'Apple A15 GPU',
            shadingLanguageVersion: 'WebGL GLSL ES 3.00',
            version: 'WebGL 2.0',
            maxVertexAttribs: 16,
            maxTextureSize: 16384,
            maxViewportDims: [16384, 16384]
        },
        'iPhone 14': {
            vendor: 'Apple Inc.',
            renderer: 'Apple A15 GPU',
            shadingLanguageVersion: 'WebGL GLSL ES 3.00',
            version: 'WebGL 2.0',
            maxVertexAttribs: 16,
            maxTextureSize: 16384,
            maxViewportDims: [16384, 16384]
        },
        'iPhone 15': {
            vendor: 'Apple Inc.',
            renderer: 'Apple A16 GPU',
            shadingLanguageVersion: 'WebGL GLSL ES 3.00',
            version: 'WebGL 2.0',
            maxVertexAttribs: 16,
            maxTextureSize: 16384,
            maxViewportDims: [16384, 16384]
        }
    };

    const getDeviceName = () => {
        if (typeof deviceName !== 'undefined' && deviceName) {
            return deviceName;
        }
        
        try {
            const ua = navigator.userAgent || '';
            if (ua.includes('iPhone')) {
                if (ua.includes('iPhone OS 17') || ua.includes('iPhone OS 18')) {
                    return 'iPhone 15';
                } else if (ua.includes('iPhone OS 16')) {
                    return 'iPhone 14';
                } else if (ua.includes('iPhone OS 15')) {
                    return 'iPhone 13';
                } else if (ua.includes('iPhone OS 14')) {
                    return 'iPhone 12';
                } else if (ua.includes('iPhone OS 13')) {
                    return 'iPhone 11';
                }
            }
        } catch (e) {
        }
        
        return 'iPhone 13';
    };

    const detectedDeviceName = getDeviceName();
    const config = gpuConfigs[detectedDeviceName] || gpuConfigs['iPhone 13'];

    const UNMASKED_VENDOR_WEBGL = 37445;
    const UNMASKED_RENDERER_WEBGL = 37446;
    const VERSION = 7938;
    const SHADING_LANGUAGE_VERSION = 35724;
    const MAX_VERTEX_ATTRIBS = 34921;
    const MAX_TEXTURE_SIZE = 3379;
    const MAX_VIEWPORT_DIMS = 3386;

    const getParameterProxyHandler = {
        apply: function (target, ctx, args) {
            const param = (args || [])[0];
            const result = utils.cache.Reflect.apply(target, ctx, args);

            if (param === UNMASKED_VENDOR_WEBGL) {
                return config.vendor;
            }
            if (param === UNMASKED_RENDERER_WEBGL) {
                return config.renderer;
            }
            if (param === VERSION) {
                return config.version;
            }
            if (param === SHADING_LANGUAGE_VERSION) {
                return config.shadingLanguageVersion;
            }
            if (param === MAX_VERTEX_ATTRIBS) {
                return config.maxVertexAttribs;
            }
            if (param === MAX_TEXTURE_SIZE) {
                return config.maxTextureSize;
            }
            if (param === MAX_VIEWPORT_DIMS) {
                return new Int32Array(config.maxViewportDims);
            }

            return result;
        }
    };

    const addProxy = (object, property_name) => {
        utils.replaceWithProxy(object, property_name, getParameterProxyHandler);
    };

    addProxy(WebGLRenderingContext.prototype, 'getParameter');
    addProxy(WebGL2RenderingContext.prototype, 'getParameter');
    
    const originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(contextType, ...args) {
        const context = originalGetContext.call(this, contextType, ...args);
        if (context && (contextType === 'webgl' || contextType === 'webgl2' || contextType === 'experimental-webgl')) {
            const originalGetParam = context.getParameter;
            context.getParameter = function(param) {
                if (param === UNMASKED_VENDOR_WEBGL) {
                    return config.vendor;
                }
                if (param === UNMASKED_RENDERER_WEBGL) {
                    return config.renderer;
                }
                if (param === VERSION) {
                    return config.version;
                }
                if (param === SHADING_LANGUAGE_VERSION) {
                    return config.shadingLanguageVersion;
                }
                return originalGetParam.call(this, param);
            };
        }
        return context;
    };

    const getExtensionProxyHandler = {
        apply: function (target, ctx, args) {
            const extensionName = (args || [])[0];
            const result = utils.cache.Reflect.apply(target, ctx, args);
            
            if (extensionName === 'WEBGL_debug_renderer_info') {
                const debugInfo = result || {};
                Object.defineProperty(debugInfo, 'UNMASKED_VENDOR_WEBGL', {
                    get: () => 37445,
                    configurable: true,
                    enumerable: true
                });
                Object.defineProperty(debugInfo, 'UNMASKED_RENDERER_WEBGL', {
                    get: () => 37446,
                    configurable: true,
                    enumerable: true
                });
                
                const originalGetParam = debugInfo.getParameter;
                if (originalGetParam) {
                    debugInfo.getParameter = function(param) {
                        if (param === 37445) return config.vendor;
                        if (param === 37446) return config.renderer;
                        return originalGetParam.call(this, param);
                    };
                } else {
                    debugInfo.getParameter = function(param) {
                        if (param === 37445) return config.vendor;
                        if (param === 37446) return config.renderer;
                        return null;
                    };
                }
                
                return debugInfo;
            }
            
            return result;
        }
    };

    addProxy(WebGLRenderingContext.prototype, 'getExtension');
    addProxy(WebGL2RenderingContext.prototype, 'getExtension');
    
    try {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (gl) {
            const originalGetParam = gl.getParameter;
            gl.getParameter = function(param) {
                if (param === UNMASKED_VENDOR_WEBGL) {
                    return config.vendor;
                }
                if (param === UNMASKED_RENDERER_WEBGL) {
                    return config.renderer;
                }
                return originalGetParam.call(this, param);
            };
            
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            if (debugInfo) {
                Object.defineProperty(debugInfo, 'UNMASKED_VENDOR_WEBGL', {
                    get: () => 37445,
                    configurable: true,
                    enumerable: true
                });
                Object.defineProperty(debugInfo, 'UNMASKED_RENDERER_WEBGL', {
                    get: () => 37446,
                    configurable: true,
                    enumerable: true
                });
            }
        }
    } catch (e) {
    }
    
    const spoofExistingContexts = () => {
        try {
            const canvases = document.querySelectorAll('canvas');
            canvases.forEach(canvas => {
                try {
                    const gl = canvas.getContext('webgl') || canvas.getContext('webgl2') || canvas.getContext('experimental-webgl');
                    if (gl) {
                        const originalGetParam = gl.getParameter;
                        gl.getParameter = function(param) {
                            if (param === UNMASKED_VENDOR_WEBGL) return config.vendor;
                            if (param === UNMASKED_RENDERER_WEBGL) return config.renderer;
                            return originalGetParam.call(this, param);
                        };
                    }
                } catch (e) {}
            });
        } catch (e) {}
    };
    
    spoofExistingContexts();
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', spoofExistingContexts);
    }
    
    if (document.body || document.documentElement) {
        try {
            const observer = new MutationObserver(() => {
                spoofExistingContexts();
            });
            observer.observe(document.body || document.documentElement, {
                childList: true,
                subtree: true
            });
        } catch (e) {}
    }
})();

