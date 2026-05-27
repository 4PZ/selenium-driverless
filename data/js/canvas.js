const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;

const canvasFingerprintCache = new Map();

HTMLCanvasElement.prototype.toDataURL = function (type, ...args) {
    if (type === undefined) {
        type = 'image/png'; 
    }

    const originalBase64 = originalToDataURL.call(this, type, ...args);
    if (canvasFingerprintCache.has(originalBase64)) {
        console.log("Returning cached modified Base64 for this canvas.");
        return canvasFingerprintCache.get(originalBase64);
    }

    let isFingerprintAttempt =
        type === 'image/png' && 
        this.width > 0 && this.width <= 300 && 
        this.height > 0 && this.height <= 300

    
    if (isFingerprintAttempt) {
        let originalBase64 = originalToDataURL.call(this, type, ...args);

        const ctx = this.getContext("2d");
        const imageData = ctx.getImageData(0, 0, this.width, this.height);
       
        let randomIndex = Math.floor(Math.random() * imageData.data.length / 4) * 4;
        imageData.data[randomIndex] = Math.floor(Math.random() * 255); 
        imageData.data[randomIndex + 1] = Math.floor(Math.random() * 255); 
        imageData.data[randomIndex + 2] = Math.floor(Math.random() * 255); 

        const clonedCanvas = document.createElement("canvas");
        const newCtx = clonedCanvas.getContext("2d");
        clonedCanvas.width = this.width;
        clonedCanvas.height = this.height;
        newCtx.putImageData(imageData, 0, 0);

        const originalClonedToDataURL = clonedCanvas.toDataURL;
        clonedCanvas.toDataURL = originalToDataURL;

        const modifiedBase64 = clonedCanvas.toDataURL(type);

        clonedCanvas.toDataURL = originalClonedToDataURL;
        canvasFingerprintCache.set(originalBase64, modifiedBase64);

        return modifiedBase64;
    }

    return originalToDataURL.apply(this, [type, ...args]);
};