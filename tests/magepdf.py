from pypdf import PdfMerger

pdfs = [r'C:\Users\Jian Qiu\Dropbox\Passport_File\Qiujian\US_Visa_1.pdf',
        r'C:\Users\Jian Qiu\Dropbox\Passport_File\Qiujian\US_Visa_2.pdf',
        r'C:\Users\Jian Qiu\Dropbox\Passport_File\Qiujian\US_Visa_3.pdf']

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write(r"C:\Users\Jian Qiu\Dropbox\Passport_File\Qiujian\result_merged_visa.pdf")
merger.close()