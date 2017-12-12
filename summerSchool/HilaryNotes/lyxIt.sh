#!/bin/bash -e

file=WellerSSnotes

if [ -e ${file}.pdf ]; then
    rm ${file}.pdf
fi

# function to change directory names into file names
function makeFileName {
    fullName=$1
    # strip home directory and opening dots out of file name
    name=`echo $fullName | sed 's/\/home\/hilary\///g' | sed 's/\.\.\///g' \
         | sed 's/\.\.\///g' | sed 's/\.\.\///g' | sed 's/\.\.\///g' \
         | sed 's/\.\.\///g' | sed 's/\.\.\///g' | sed 's/\.\.\///g' \
         | sed 's/\.\///g' | sed 's/OpenFOAM\/hilary-.\..\..\/run\///g' | sed 's/\//_/g'`
    echo $name
}

# copy animations to the animations directory
animations="/home/hilary/OpenFOAM/hilary-2.3.0/run/teachingAnims/advection/movie/T.mp4
            /home/hilary/Videos/pollutionPlumes/pollutionPlumes.avi
            /home/hilary/latex/teaching/MPECDT/PDEsNumerics/notes/anims/Spherical_wave2.avi
            /home/hilary/Videos/pressureWaves/bombBlast.avi
            /home/hilary/Videos/geoTurbulence/geoTurbulence.avi
            /home/hilary/Videos/damBreak/damBreak.avi
            /home/hilary/Videos/convectivePlumes/explosiveComulonumbus.avi
            /home/hilary/latex/teaching/MTMW12/2014/notes/pythonExamples/diffusion/FTCSdiffusion.avi
            /home/hilary/Videos/NUGAM/NUGAM_Sun_1yr_web.avi
            /home/hilary/latex/teaching/MTMW12/2014/notes/anims/FTBS.mp4
            /home/hilary/latex/teaching/MTMW12/2014/notes/anims/FTBS_CTCS.mp4
            ../../../../teaching/MTMW12/2014/notes/anims/Fourier/Periodic_identity_function.mp4
            ../../../../teaching/MTMW12/2014/notes/anims/Fourier/Fourier_series_square_wave_circles_animation.mp4
            ../../../../teaching/MTMW12/2014/notes/anims/Fourier/Fourier_series_sawtooth_wave_circles_animation.mp4"

for animFile in $animations; do
    cpFile=`makeFileName $animFile`
    cp -u $animFile animations/$cpFile
done


# create the online version
sed 's/%VERSION/\\onlineversion\\studentversion/g' studentVersionTMP > studentVersion.tex
lyx --export pdflatex -f all ${file}.lyx
lualatex ${file}.tex
lualatex ${file}.tex
mv ${file}.pdf ${file}_online.pdf

# create the students version
sed 's/%VERSION/\\studentversion/g' studentVersionTMP > studentVersion.tex
lyx --export pdflatex -f all ${file}.lyx
lualatex ${file}.tex
lualatex ${file}.tex
pdfjam --nup 1x2 --scale 0.95 --a4paper $file.pdf --outfile ${file}_2_student.pdf

# create the lecturers version
cp studentVersionTMP studentVersion.tex
lyx --export pdflatex -f all ${file}.lyx
lualatex ${file}.tex
lualatex ${file}.tex
pdfjam --nup 1x2 --scale 0.95 --a4paper $file.pdf --outfile ${file}_2_lec.pdf

rmtexall ${file}.tex
rm $file.pdf

#okular *pdf &

## tar and gzip the necessary stuff
#tar cvf - *pdf animations practicals/linearAdvectCode/ practicals/SWE \
#    | gzip -c > Weller_summerSchool.tar.gz

file=feedback

# create the online version
sed 's/%VERSION/\\onlineversion\\studentversion/g' studentVersionTMP > studentVersion.tex
lyx --export pdflatex -f all ${file}.lyx
lualatex ${file}.tex
lualatex ${file}.tex
mv ${file}.pdf ${file}_online.pdf

# create the students version
sed 's/%VERSION/\\studentversion/g' studentVersionTMP > studentVersion.tex
lyx --export pdflatex -f all ${file}.lyx
lualatex ${file}.tex
lualatex ${file}.tex
pdfjam --nup 1x2 --scale 0.95 --a4paper $file.pdf --outfile ${file}_2_student.pdf

rmtexall ${file}.tex
rm $file.pdf

