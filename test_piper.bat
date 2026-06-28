@echo off

echo नमस्कार सभी | tools\piper\piper.exe ^
--model models\piper\hi_IN-pratham-medium.onnx ^
--output_file storage\audio_output\test_hindi.wav

pause