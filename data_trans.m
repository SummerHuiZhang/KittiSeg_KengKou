file = dir('/Users/zhanghui/Documents/kengkou/*_json');
abs = which('data_trans');
abs_rou=strrep(abs,'data_trans.m','Annotation/');
img =strrep(abs,'data_trans.m','Image/');
for n=1:length(file)
    str1 =[file(n).name,'/label.png'];
    str2 =[file(n).name,'/img.png'];
    a = imread(str1);
    b = imread(str2);

    R = b(:,:,1);
    G = b(:,:,2);
    B = b(:,:,3);
    R(a>0) =255;
    R(a<1)=0;
    G(a>-1)=0;
    B(a>-1)=0;
   
    image = cat(3,R,G,B);
    new_store = strcat(file(n).name,'.png');
    %cd(abs_rou);
    imwrite(image,[abs_rou,new_store]);
    imwrite(b,[img,new_store]);
end 