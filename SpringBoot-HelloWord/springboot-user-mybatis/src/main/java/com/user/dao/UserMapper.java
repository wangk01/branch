package com.user.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import com.user.domain.User;

@Mapper
public interface UserMapper {

	@Select("select * from user where name like '%${value}%'")
	public List<User> queryUserByname(String name);
}
