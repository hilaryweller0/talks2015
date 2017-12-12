#!/bin/bash -e

file=WellerEmergingMethods

if [ -e ${file}.pdf ]; then
    rm ${file}.pdf
fi


# create the online version
sed 's/%VERSION/\\onlineversion\\studentversion/g' studentVersionTMP > studentVersion.tex
lyx --export pdflatex -f all ${file}.lyx
lualatex ${file}.tex
lualatex ${file}.tex
mv ${file}.pdf ${file}_online.pdf

## create the students version
#sed 's/%VERSION/\\studentversion/g' studentVersionTMP > studentVersion.tex
#lyx --export pdflatex -f all ${file}.lyx
#lualatex ${file}.tex
#lualatex ${file}.tex
#pdfjam --nup 1x2 --a4paper $file.pdf --outfile ${file}_2_student.pdf

## create the lecturers version
#cp studentVersionTMP studentVersion.tex
#lyx --export pdflatex -f all ${file}.lyx
#lualatex ${file}.tex
#lualatex ${file}.tex
#pdfjam --nup 1x2 --a4paper $file.pdf --outfile ${file}_2_lec.pdf

#rmtexall ${file}.tex
#rm $file.pdf

##okular *pdf &

