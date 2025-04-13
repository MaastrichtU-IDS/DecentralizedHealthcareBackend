from wordcloud import WordCloud


import matplotlib.pyplot as plt
import os

print(os.getcwd())
# Sample ICD-10 codes
icd10_codes = [
    'A00', 'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09',
    'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19',
    'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29',
    'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39',
    'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47', 'A48', 'A49',
    'B00', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09',
    'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19',
    'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29',
    'B30', 'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37', 'B38', 'B39',
    'C00', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09'
    'D00', 'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09',
    'E00', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09',
    'F00', 'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09',
    'Z00', 'Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'Z07', 'Z08', 'Z09',
    'Z10', 'Z11', 'Z12', 'Z13', 'Z14', 'Z15', 'Z16', 'Z17', 'Z18', 'Z19',
    'Z20', 'Z21', 'Z22', 'Z23', 'Z24', 'Z25', 'Z26', 'Z27', 'Z28', 'Z29',
    'Z30', 'Z31', 'Z32', 'Z33', 'Z34', 'Z35', 'Z36', 'Z37', 'Z38', 'Z39',
    'Z40', 'Z41', 'Z42', 'Z43', 'Z44', 'Z45', 'Z46', 'Z47', 'Z48', 'Z49',
    'Z90', 'Z91', 'Z92', 'Z93', 'Z94', 'Z95', 'Z96', 'Z97', 'Z98', 'Z99'
    
]

# Join the codes into a single string
text = ' '.join(icd10_codes)
font_path = "c:\WINDOWS\Fonts\MSYHBD.TTC"

# Generate the word cloud
wordcloud = WordCloud(width=4800, height=2400, background_color='white', font_path=font_path).generate(text)

# Plot the word cloud
plt.figure(figsize=(40, 20),dpi=600)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
# plt.title('ICD-10 Codes')
plt.savefig('jupyter/figs/icd10_codes_word_cloud.pdf')
plt.show()
