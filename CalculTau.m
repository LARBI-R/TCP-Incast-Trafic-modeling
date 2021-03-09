% non linear regression
S = 1446 *8 ;
SRU = 256000*8;

T = readtable('simus.csv');

%% TCP RENO FIFO
Ci = 10^6 *  table2array(T(1:15492,'C'));
Ni = table2array(T(1:15492,'N'));
fcti =10^(-3) * table2array(T(1:15492,'fct'));
x1 = Ni ( : , 1) ;                                           % Independent Variable Vector
x2 = Ci ( :, 1 );                                              % Independent Variable Vector
y  =  fcti ( :,  1 );                                             % Dependent Variable Vector

xm = [x1(:) x2(:)];                                                % X Matrix

yfcn = @(b,x) ( b(1).*x(:,1) ).*b(2)./(x(:,2));       % Objective Function
b0 = [SRU/S; S];

% COEF equation FIFO
B_FIFO = lsqcurvefit(yfcn,b0,xm,y(:))
%% TCP RENO FQ
Ci = 10^6 *  table2array(T(15493:30994,'C'));
Ni = table2array(T(15493:30994,'N'));
fcti =10^(-3) * table2array(T(15493:30994,'fct'));
x1 = Ni ( : , 1) ;                                           % Independent Variable Vector
x2 = Ci ( :, 1 );                                              % Independent Variable Vector
y  =  fcti ( :,  1 );                                             % Dependent Variable Vector

xm = [x1(:) x2(:)];                                                % X Matrix

yfcn = @(b,x) ( b(1).*x(:,1) ).*b(2)./(x(:,2));       % Objective Function
b0 = [SRU/S; S];

% COEF equation FQ
B_FQ = lsqcurvefit(yfcn,b0,xm,y(:))

%% TCP DCTCP
Ci = 10^6 *  table2array(T(30995:46581,'C'));
Ni = table2array(T(30995:46581,'N'));
fcti =10^(-3) * table2array(T(30995:46581,'fct'));
x1 = Ni ( : , 1) ;                                           % Independent Variable Vector
x2 = Ci ( :, 1 );                                              % Independent Variable Vector
y  =  fcti ( :,  1 );                                             % Dependent Variable Vector

xm = [x1(:) x2(:)];                                                % X Matrix

yfcn = @(b,x) ( b(1).*x(:,1) ).*b(2)./(x(:,2));       % Objective Function
b0 = [SRU/S; S];

% COEF equation DCTCP
B_DCTCP = lsqcurvefit(yfcn,b0,xm,y(:))
