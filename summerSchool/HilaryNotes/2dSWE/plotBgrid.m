function var_list = plotBgrid(phi, u, v, it)

% write a netcdf files of the data

nc = netcdf('Bgridu.nc', 'c');
nc('x') = size(u,2);
nc('y') = size(u,1);
nc{'u'} = ncdouble('x', 'y');
nc{'u'}(:) = u';
close(nc);

nc = netcdf('Bgridv.nc', 'c');
nc('x') = size(v,2);
nc('y') = size(v,1);
nc{'v'} = ncdouble('x', 'y');
nc{'v'}(:) = v';
close(nc);

nc = netcdf('Bgridphi.nc', 'c');
nc('x') = size(phi,2);
nc('y') = size(phi,1);
nc{'p'} = ncdouble('x', 'y');
nc{'p'}(:) = phi';
close(nc);

sysCommand = sprintf("grdimage Bgridphi.nc -C$GMTU/colours/red_white_blue.cpt -JX15c/15c -R0.5/9.5/0.5/9.5 -Bg1+0.5 -K >Bgrid%d.eps", it);
system(sysCommand);

sysCommand = sprintf("grdvector Bgridu.nc Bgridv.nc -S0.1 -Q+e+n -J -R1/10/1/10 -W1pt -O >> Bgrid%d.eps", it);
system(sysCommand);

system(sprintf("makebb Bgrid%d.eps", it));

%system(sprintf("gv Bgrid%d.eps", it));


