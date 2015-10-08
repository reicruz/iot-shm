m=csvread('json_class5.csv');
fs=1600;
n=64;
freq=[];
j=sqrt(-1);
for i=1:n/2-1
    freq=[freq i*fs/n];
end
m_size=size(m);
figure
for r=1:m_size(1)
    mag_vec=[];
    for i=2:m_size(2)
        mag_vec=[mag_vec m(r,i)];
    end
    r
    plot(freq, mag_vec,'*')
    hold on
end
