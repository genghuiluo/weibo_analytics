-- clean device
select case locate('来自',device) 
    when 0 then NULL 
    else substring(device,locate('来自',device)+2,length(device)-locate('来自',device)) 
    end as clean_device,
    count(*) 
from weibo_posts group by 1;

-- classifieds
select
    device,
    case locate('来自',device) 
        when 0 then NULL 
        else substring(device,locate('来自',device)+2,length(device)-locate('来自',device)) 
    end as clean_device,
    case when locate('iPhone',device)<>0 or locate('iOS',device) then 'iPhone'
        when locate('iPad',device)<>0 then 'iPad'
        when locate('Android',device)<>0 then 'Android'
        when locate('OPPO',device)<>0 or locate('vivo',device)<>0 then 'OPPO'
        when locate('三星',device)<>0 or locate('Galaxy',device)<>0 then 'Samsung'
        when locate('HUAWEI',device)<>0 or locate('荣耀',device)<>0 or locate('华为',device)<>0 then '华为'
        when locate('魅蓝',device)<>0 or locate('魅族',device)<>0 or locate('Flyme',device)<>0 then '魅族'
        when locate('小米',device)<>0 or locate('红米',device)<>0 then '小米'
        when locate('乐',device)<>0 then '乐视'
        when locate('Smartisan',device)<>0 or locate('坚果',device)<>0 then '锤子科技'
        when locate('美图',device)<>0 then '美图'
        when locate('nubia',device)<>0 or locate('努比亚',device)<>0 then '锤子科技'
        when locate('360',device)<>0 or locate('大神',device)<>0 or locate('酷派',device)<>0 or locate('360',device)<>0 then '360'
        when locate('中兴',device)<>0 or locate('ZTE',device)<>0 then '中兴'
        when locate('联想',device)<>0 or locate('ZUK',device)<>0 then '联想'
        when locate('HTC',device)<>0 then 'HTC'
        when locate('OnePlus',device)<>0 or locate('一加',device)<>0 then '一加'
        when locate('weibo.com',device)<>0 or locate('网页版',device)<>0 or locate('电脑',device)<>0 then 'Web'
    else case locate('来自',device) 
            when 0 then NULL 
            else substring(device,locate('来自',device)+2,length(device)-locate('来自',device)) 
        end
    end as classifieds,
from weibo_posts;

-- check classifieds rules
select
    case when locate('iPhone',device)<>0 or locate('iOS',device) then 'iPhone'
        when locate('iPad',device)<>0 then 'iPad'
        when locate('Android',device)<>0 then 'Android'
        when locate('OPPO',device)<>0 or locate('vivo',device)<>0 then 'OPPO'
        when locate('三星',device)<>0 or locate('Galaxy',device)<>0 then 'Samsung'
        when locate('HUAWEI',device)<>0 or locate('荣耀',device)<>0 or locate('华为',device)<>0 then '华为'
        when locate('魅蓝',device)<>0 or locate('魅族',device)<>0 or locate('Flyme',device)<>0 then '魅族'
        when locate('小米',device)<>0 or locate('红米',device)<>0 then '小米'
        when locate('乐',device)<>0 then '乐视'
        when locate('Smartisan',device)<>0 or locate('坚果',device)<>0 then '锤子科技'
        when locate('美图',device)<>0 then '美图'
        when locate('nubia',device)<>0 or locate('努比亚',device)<>0 then '锤子科技'
        when locate('360',device)<>0 or locate('大神',device)<>0 or locate('酷派',device)<>0 or locate('360',device)<>0 then '360'
        when locate('中兴',device)<>0 or locate('ZTE',device)<>0 then '中兴'
        when locate('联想',device)<>0 or locate('ZUK',device)<>0 then '联想'
        when locate('HTC',device)<>0 then 'HTC'
        when locate('OnePlus',device)<>0 or locate('一加',device)<>0 then '一加'
        when locate('weibo.com',device)<>0 or locate('网页版',device)<>0 or locate('电脑',device)<>0 then 'Web'
    else case locate('来自',device) 
            when 0 then NULL 
            else substring(device,locate('来自',device)+2,length(device)-locate('来自',device)) 
        end
    end as classifieds,
    count(*) as cnt,
    count(*)/(select count(*) from weibo_posts) as percent 
from weibo_posts
group by 1
order by 2 desc;

