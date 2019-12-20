import os

import six
import pytest

from thumbor.context import Context, RequestParameters, ServerParameters
from thumbor.importer import Importer
from thumbor.server import configure_log
from thumbor.utils import which

import thumbor_video_engine.engines.ffmpeg
from thumbor_video_engine.engines.ffmpeg import Engine


@pytest.fixture
def context(config):
    config.ENGINE = 'thumbor_video_engine.engines.ffmpeg'

    importer = Importer(config)
    importer.import_modules()

    req = RequestParameters()

    server = ServerParameters(8080, 'localhost', 'thumbor.conf', None, 'info', None)
    server.security_key = config.SECURITY_KEY
    server.gifsicle_path = which('gifsicle')

    context = Context(server=server, config=config, importer=importer)
    context.request = req
    context.request.engine = context.modules.engine

    configure_log(config, 'DEBUG')
    return context


@pytest.fixture
def mp4_buffer(storage_path):
    with open(os.path.join(storage_path, 'hotdog.mp4'), mode='rb') as f:
        return f.read()


@pytest.fixture
def mock_engine(context, mp4_buffer, mocker):
    class MockNamedTemporaryFile(mocker.Mock):
        def __init__(self, suffix=None, **kwargs):
            super(MockNamedTemporaryFile, self).__init__(**kwargs)
            suffix = suffix or ''
            self.name = '/tmp/tempfile%s' % suffix

    engine = Engine(context)

    mocker.patch.object(engine, 'ffprobe')
    mocker.patch.object(thumbor_video_engine.engines.ffmpeg, 'NamedTemporaryFile',
        wraps=MockNamedTemporaryFile)
    mocker.patch.object(six.moves.builtins, 'open', new_callable=mocker.mock_open())
    mocker.patch.object(os, 'unlink')
    mocker.patch.object(engine, 'run_cmd', return_value=mp4_buffer)

    engine.load(mp4_buffer, '.mp4')
    engine.fps = 33.3333
    engine.width = engine.source_width = 200
    engine.height = engine.source_height = 150
    engine.image_size = (200, 150)

    return engine


@pytest.fixture
def std_flags():
    return [
        '-an', '-pix_fmt', 'yuv420p', '-movflags', 'faststart',
        '-vf', 'rotate=0,crop=1:1:0:0,scale=200:150:flags=lanczos',
    ]


@pytest.fixture
def std_h264_flags(ffmpeg_path, std_flags):
    return [
        ffmpeg_path, '-hide_banner', '-i', '/tmp/tempfile.mp4',
        '-c:v', 'libx264'
    ] + std_flags + ['-f', 'mp4']


@pytest.fixture
def std_h265_flags(ffmpeg_path, std_flags):
    return [
        ffmpeg_path, '-hide_banner', '-i', '/tmp/tempfile.mp4',
        '-c:v', 'hevc', '-tag:v', 'hvc1',
    ] + std_flags + ['-f', 'mp4']


@pytest.fixture
def std_vp9_flags(ffmpeg_path, std_flags):
    return [
        ffmpeg_path, '-hide_banner', '-i', '/tmp/tempfile.mp4',
        '-c:v', 'libvpx-vp9', '-loop', '0',
    ] + std_flags + ['-f', 'webm']


def test_h264_two_pass(mock_engine, std_h264_flags, mocker):
    mock_engine.context.request.format = 'h264'
    mock_engine.context.config.FFMPEG_H264_TWO_PASS = True

    mock_engine.read('.mp4', quality=80)

    assert mock_engine.run_cmd.mock_calls == [
        mocker.call(std_h264_flags + [
            '-pass', '1', '-passlogfile', '/tmp/tempfile.log', '-y', '/dev/null']),
        mocker.call(std_h264_flags + [
            '-pass', '2', '-passlogfile', '/tmp/tempfile.log', '-y', '/tmp/tempfile.mp4'])]


def test_h265_two_pass(mock_engine, std_h265_flags, mocker):
    mock_engine.context.request.format = 'h265'
    mock_engine.context.config.FFMPEG_H265_TWO_PASS = True

    mock_engine.read('.mp4', quality=80)

    assert mock_engine.run_cmd.mock_calls == [
        mocker.call(std_h265_flags + [
            '-x265-params', 'pass=1:stats=/tmp/tempfile.log', '-y', '/dev/null']),
        mocker.call(std_h265_flags + [
            '-x265-params', 'pass=2:stats=/tmp/tempfile.log', '-y', '/tmp/tempfile.mp4'])]


def test_vp9_two_pass(mock_engine, std_vp9_flags, mocker):
    mock_engine.context.request.format = 'vp9'
    mock_engine.context.config.FFMPEG_VP9_TWO_PASS = True

    mock_engine.read('.mp4', quality=80)

    assert mock_engine.run_cmd.mock_calls == [
        mocker.call(std_vp9_flags + [
            '-pass', '1', '-passlogfile', '/tmp/tempfile.log', '-y', '/dev/null']),
        mocker.call(std_vp9_flags + [
            '-pass', '2', '-passlogfile', '/tmp/tempfile.log', '-y', '/tmp/tempfile.webm'])]


@pytest.mark.parametrize("config_key,config_val,expected", [
    ('FFMPEG_H264_CRF', '22', ['-crf', '22']),
    ('FFMPEG_H264_VBR', '1M', ['-b:v', '1M']),
    ('FFMPEG_H264_PROFILE', 'high', ['-profile:v', 'high']),
    ('FFMPEG_H264_PRESET', 'medium', ['-preset', 'medium']),
    ('FFMPEG_H264_LEVEL', '3.0', ['-level', '3.0']),
    ('FFMPEG_H264_TUNE', 'film', ['-tune', 'film']),
    ('FFMPEG_H264_MAXRATE', '2M', ['-maxrate', '2M']),
    ('FFMPEG_H264_BUFSIZE', '4M', ['-bufsize', '4M']),
    ('FFMPEG_H264_QMIN', '16', ['-qmin', '16']),
    ('FFMPEG_H264_QMAX', '26', ['-qmax', '26']),
])
def test_h264_config(config_key, config_val, expected, mock_engine, std_h264_flags, mocker):
    mock_engine.context.request.format = 'h264'
    setattr(mock_engine.context.config, config_key, config_val)

    mock_engine.read('.mp4', quality=80)

    assert mock_engine.run_cmd.mock_calls == [
        mocker.call(std_h264_flags + expected + ['-y', '/tmp/tempfile.mp4']),
    ]


@pytest.mark.parametrize("config_key,config_val,expected", [
    ('FFMPEG_H265_VBR', '1M', ['-b:v', '1M']),
    ('FFMPEG_H265_CRF', '22', ['-crf', '22']),
    ('FFMPEG_H265_PROFILE', 'high', ['-profile:v', 'high']),
    ('FFMPEG_H265_PRESET', 'medium', ['-preset', 'medium']),
    ('FFMPEG_H265_TUNE', 'film', ['-tune', 'film']),
    ('FFMPEG_H265_MAXRATE', '2M', ['-x265-params', 'vbv-maxrate=2M']),
    ('FFMPEG_H265_BUFSIZE', '4M', ['-x265-params', 'vbv-bufsize=4M']),
    ('FFMPEG_H265_CRF_MIN', '16', ['-x265-params', 'crf-min=16']),
    ('FFMPEG_H265_CRF_MAX', '26', ['-x265-params', 'crf-max=26']),
])
def test_h265_config(config_key, config_val, expected, mock_engine, std_h265_flags, mocker):
    mock_engine.context.request.format = 'h265'
    setattr(mock_engine.context.config, config_key, config_val)

    mock_engine.read('.mp4', quality=80)

    if '-x265-params' not in expected:
        expected += ['-x265-params', '']

    assert mock_engine.run_cmd.mock_calls == [
        mocker.call(std_h265_flags + expected + ['-y', '/tmp/tempfile.mp4']),
    ]


@pytest.mark.parametrize("config_key,config_val,expected", [
    ('FFMPEG_VP9_CRF', '22', ['-crf', '22']),
    ('FFMPEG_VP9_VBR', '1M', ['-b:v', '1M']),
    ('FFMPEG_VP9_DEADLINE', 'high', ['-deadline', 'high']),
    ('FFMPEG_VP9_CPU_USED', '4', ['-cpu-used', '4']),
    ('FFMPEG_VP9_ROW_MT', True, ['-row-mt', '1']),
    ('FFMPEG_VP9_LOSSLESS', True, ['-lossless', '1']),
    ('FFMPEG_VP9_MAXRATE', '4M', ['-maxrate', '4M']),
    ('FFMPEG_VP9_MINRATE', '1M', ['-minrate', '1M']),
])
def test_vp9_config(config_key, config_val, expected, mock_engine, std_vp9_flags, mocker):
    mock_engine.context.request.format = 'vp9'
    setattr(mock_engine.context.config, config_key, config_val)

    mock_engine.read('.mp4', quality=80)

    assert mock_engine.run_cmd.mock_calls == [
        mocker.call(std_vp9_flags + expected + ['-y', '/tmp/tempfile.webm']),
    ]