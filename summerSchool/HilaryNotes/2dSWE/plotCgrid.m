function var_list = plotCgrid(phi, u, v, it)

% first create matrices for v at u and u at v

vu = zeros(size(u));
uv = zeros(size(v));

for i = 2:size(v,1)-1; for j = 1:size(u,2)-1;
    vu(i,j) = 0.25*(v(i-1,j) + v(i,j) + v(i-1,j+1) + v(i,j+1));
endfor; endfor

for i = 1:size(v,1)-1; for j = 2:size(u,2)-1;
    uv(i,j) = 0.25*(u(i,j-1) + u(i+1,j-1) + u(i,j) + u(i+1,j));
endfor; endfor

% write a netcdf files of the data

nc = netcdf('Cgridu.nc', 'c');
nc('x') = size(u,2);
nc('y') = size(u,1);
nc{'u'} = ncdouble('x', 'y');
nc{'u'}(:) = u';
close(nc);

nc = netcdf('Cgriduv.nc', 'c');
nc('x') = size(uv,2);
nc('y') = size(uv,1);
nc{'u'} = ncdouble('x', 'y');
nc{'u'}(:) = uv';
close(nc);

nc = netcdf('Cgridv.nc', 'c');
nc('x') = size(v,2);
nc('y') = size(v,1);
nc{'v'} = ncdouble('x', 'y');
nc{'v'}(:) = v';
close(nc);

nc = netcdf('Cgridvu.nc', 'c');
nc('x') = size(vu,2);
nc('y') = size(vu,1);
nc{'v'} = ncdouble('x', 'y');
nc{'v'}(:) = vu';
close(nc);

nc = netcdf('Cgridphi.nc', 'c');
nc('x') = size(phi,2);
nc('y') = size(phi,1);
nc{'p'} = ncdouble('x', 'y');
nc{'p'}(:) = phi';
close(nc);

sysCommand = sprintf("grdimage Cgridphi.nc -C$GMTU/colours/red_white_blue.cpt -JX15c/15c -R0.5/9.5/0.5/9.5 -Bg1+0.5 -K >Cgrid%d.eps", it);
system(sysCommand);

sysCommand = sprintf("grdvector Cgridu.nc Cgridvu.nc -S0.1 -Q+e+n -J -R1/10/0.5/9.5 -W1pt -O -K >> Cgrid%d.eps", it);
system(sysCommand);

sysCommand = sprintf("grdvector Cgriduv.nc Cgridv.nc -S0.1 -Q+e+n -J -R0.5/9.5/1/10 -W1pt -O >> Cgrid%d.eps", it);
system(sysCommand);

system(sprintf("makebb Cgrid%d.eps", it));

%system(sprintf("gv Cgrid%d.eps", it));


