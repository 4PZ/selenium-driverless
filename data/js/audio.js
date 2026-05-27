(function() {
    const originalGetChannelData = AudioBuffer.prototype.getChannelData;
    AudioBuffer.prototype.getChannelData = function() {
        const data = originalGetChannelData.apply(this, arguments);
        for (let i = 0; i < data.length; i++) {
            data[i] += Math.random() * 0.0001; 
        }
        return data;
    };

    const originalCreateAnalyser = AudioContext.prototype.createAnalyser;
    AudioContext.prototype.createAnalyser = function() {
        const analyser = originalCreateAnalyser.apply(this, arguments);
        const originalGetByteFrequencyData = analyser.getByteFrequencyData;
        analyser.getByteFrequencyData = function(array) {
            originalGetByteFrequencyData.call(this, array);
            for (let i = 0; i < array.length; i++) {
                array[i] += Math.random() * 2; 
            }
        };
        return analyser;
    };
})();