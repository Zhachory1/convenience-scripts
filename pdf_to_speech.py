# Convert PDF to TTS mp3, split by page

from absl import app
from absl import flags
from PyPDF4 import PdfFileReader
from gtts import gTTS
from gtts import lang


FLAGS = flags.FLAGS
flags.DEFINE_string('input_pdf', None, 'Path to file you want to convert')
flags.DEFINE_enum('lang', 'en', lang.tts_langs().keys(), 'Language the pdf is in.')

flags.mark_flag_as_required('input_pdf')

def pdfToAudio(file_name, lang):
    pdf = PdfFileReader(file_name)
    pdf_name = file_name.split(".")[0]
    print(pdf.getNumPages())
    for page in range(pdf.getNumPages()):
        text = pdf.getPage(page).extractText()
        tts = gTTS(text=text, lang=lang)
        tts.save(f"{pdf_name}_{page}.mp3")

def main(argv):
    pdfToAudio(FLAGS.input_pdf, FLAGS.lang)

if __name__ == '__main__':
    app.run(main)