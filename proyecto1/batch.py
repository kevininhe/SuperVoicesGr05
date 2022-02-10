from pydub import AudioSegment
  
# assign files
#input_file = "result.wav"
#input_file = "hello.mp3"
input_file = "/home/c.castrov/proyecto1/app/public/AudioFilesOrigin/file_example_OOG_1MG.ogg"
output_file = "/home/c.castrov/proyecto1/app/public/AudioFilesDestiny/result.mp3"
  
# convert mp3 file
sound = AudioSegment.from_file(input_file)
sound.export(output_file, format="mp3")
