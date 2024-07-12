



select count(*) as num,description   from  lfun_enum_value  where  enum_name like 'major%'
-- and description = '种子生产技术'

group by description having num>1 ;

-- order by  enum_name asc , enum_value asc ;

select * from  lfun_enum_value where  description in  (

'资源环境与安全大类','机械设计制造类','畜禽生产技术','能源动力与材料大类','地质类','畜牧业类','资源勘查类','生物与化工大类','农业类','装备制造大类','电力技术类','建筑设计类','水利大类','农林牧渔大类','水文水资源类','轻工纺织大类','土木建筑大类','林业生产技术','种子生产技术','国土资源调查','发电厂及变电站运行与维护','渔业类','林业类','作物生产技术'
  ) order by  id desc ;


--   delete from lfun_enum_value where id in  (4425, 4420,4419,4418,4417,4416,4415,4414,4413,4412,4411,4410,4409,4408,4407,4406,4405,4404,4319,4294,4293,4421,4422,4423,4424 )

