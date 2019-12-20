from thumbor.config import Config


Config.define(
    'IMAGE_ENGINE',
    'thumbor.engines.pil',
    'The engine to use for non-video files',
    'Imaging')

Config.define(
    'FFMPEG_ENGINE',
    'thumbor_video_engine.engines.ffmpeg',
    'The engine to use for video files',
    'Video')

Config.define(
    'FFMPEG_USE_GIFSICLE_ENGINE',
    False,
    'Equivalent to USE_GIFSICLE_ENGINE, but for the ffmpeg engine',
    'Video')

Config.define(
    'FFMPEG_HANDLE_ANIMATED_GIF',
    True,
    'Whether to process animated gifs with the ffmpeg engine',
    'Video')

Config.define(
    'FFPROBE_PATH',
    '/usr/local/bin/ffprobe',
    'Path for the ffprobe binary',
    'Video')

Config.define(
    'FFMPEG_H264_TWO_PASS',
    False,
    'Whether to use two-pass encoding for h264 in ffmpeg',
    'Video')

Config.define(
    'FFMPEG_H264_TWO_PASS',
    False,
    'Whether to use two-pass encoding for h264 in ffmpeg',
    'Video')

Config.define(
    'FFMPEG_H264_PRESET',
    None,
    'The -preset flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_LEVEL',
    None,
    'The -level flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_PROFILE',
    None,
    'The -profile:v flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_TUNE',
    None,
    'The -tune flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_CRF',
    None,
    'The -crf flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_VBR',
    None,
    'The average bitrate to be used by ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_MAXRATE',
    None,
    'The -maxrate flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_BUFSIZE',
    None,
    'The -bufsize flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_QMIN',
    None,
    'The -qmin flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H264_QMAX',
    None,
    'The -qmax flag passed to ffmpeg for h264 encoding',
    'Video')

Config.define(
    'FFMPEG_H265_TWO_PASS',
    False,
    'Whether to use two-pass encoding for h265 in ffmpeg',
    'Video')

Config.define(
    'FFMPEG_H265_PRESET',
    None,
    'The -preset flag passed to ffmpeg for h265 encoding',
    'Video')

Config.define(
    'FFMPEG_H265_LEVEL',
    None,
    'The -level flag passed to ffmpeg for h265 encoding',
    'Video')

Config.define(
    'FFMPEG_H265_MAXRATE',
    None,
    'The --vbv-maxrate flag passed to ffmpeg for h265 encoding',
    'Video')

Config.define(
    'FFMPEG_H265_BUFSIZE',
    None,
    'The --vbv-bufsize flag passed to libx265',
    'Video')

Config.define(
    'FFMPEG_H265_CRF_MIN',
    None,
    'The --crf-min flag passed to libx265',
    'Video')

Config.define(
    'FFMPEG_H265_CRF_MAX',
    None,
    'The --crf-max flag passed to libx265',
    'Video')

Config.define(
    'FFMPEG_H265_PROFILE',
    None,
    'The -profile:v flag passed to ffmpeg for h265 encoding',
    'Video')

Config.define(
    'FFMPEG_H265_TUNE',
    None,
    'The -tune flag passed to ffmpeg for h265 encoding',
    'Video')

Config.define(
    'FFMPEG_H265_CRF',
    None,
    'The -crf flag passed to ffmpeg for h265 encoding',
    'Video')

Config.define(
    'FFMPEG_H265_VBR',
    None,
    'The average bitrate to be used by ffmpeg for h265 encoding',
    'Video')

Config.define(
    'FFMPEG_VP9_TWO_PASS',
    False,
    'Whether to use two-pass encoding for vp9 in ffmpeg',
    'Video')

Config.define(
    'FFMPEG_VP9_VBR',
    None,
    'The average bitrate to be used by ffmpeg for vp9 encoding',
    'Video')

Config.define(
    'FFMPEG_VP9_LOSSLESS',
    False,
    'Whether to use lossless vp9 encoding',
    'Video')

Config.define(
    'FFMPEG_VP9_DEADLINE',
    None,
    'The -deadline flag passed to ffmpeg for vp9 encoding',
    'Video')

Config.define(
    'FFMPEG_VP9_CRF',
    None,
    'The constant quality (-crf) to use by ffmpeg for vp9 encoding',
    'Video')

Config.define(
    'FFMPEG_VP9_CPU_USED',
    None,
    'The -cpu-used flag passed to ffmpeg for vp9 encoding',
    'Video')

Config.define(
    'FFMPEG_VP9_ROW_MT',
    False,
    'Whether to enable row-based multithreading (-row-mt 1) for vp9 encoding in ffmpeg',
    'Video')

Config.define(
    'FFMPEG_VP9_MINRATE',
    None,
    'The -minrate flag passed to ffmpeg for vp9 encoding',
    'Video')

Config.define(
    'FFMPEG_VP9_MAXRATE',
    None,
    'The -maxrate flag passed to ffmpeg for vp9 encoding',
    'Video')