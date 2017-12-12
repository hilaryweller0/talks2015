function var_list = plotAgrid(phi, u, v, it)

% write a netcdf files of the data

nc = netcdf('Agridu.nc', 'c');
nc('x') = size(u,2);
nc('y') = size(u,1);
nc{'u'} = ncdouble('x', 'y');
nc{'u'}(:) = u';
close(nc);

nc = netcdf('Agridv.nc', 'c');
nc('x') = size(v,2);
nc('y') = size(v,1);
nc{'v'} = ncdouble('x', 'y');
nc{'v'}(:) = v';
close(nc);

nc = netcdf('Agridphi.nc', 'c');
nc('x') = size(phi,2);
nc('y') = size(phi,1);
nc{'p'} = ncdouble('x', 'y');
nc{'p'}(:) = phi';
close(nc);

sysCommand = sprintf("grdimage Agridphi.nc -C$GMTU/colours/red_white_blue.cpt -JX15c/15c -R0.5/9.5/0.5/9.5 -Bg1+0.5 -K >Agrid%d.eps", it);
system(sysCommand);

sysCommand = sprintf("grdvector Agridu.nc Agridv.nc -S0.1 -Q+e+n -J -R -W1pt -O >> Agrid%d.eps", it);
system(sysCommand);

system(sprintf("makebb Agrid%d.eps", it));

%system(sprintf("gv Agrid%d.eps &", it));


