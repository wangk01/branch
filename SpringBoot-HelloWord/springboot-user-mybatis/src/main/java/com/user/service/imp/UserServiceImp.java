package com.user.service.imp;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import com.user.dao.UserDao;
import com.user.dao.UserMapper;
import com.user.domain.User;
import com.user.service.UserService;

@Service("userService")
public class UserServiceImp implements UserService {

	@Autowired
	private UserDao userDao;
	
	@Autowired
	private UserMapper userMapper;
	
	@Override
	@Cacheable(value="findAllCache") //使用缓存并存入到redis数据库中
	//value 表示存入到redis数据库中的key
	//key  Spring 用到的，返回制定方法的key
	public List<User> findAllUser() {
		System.out.println("执行查询");
		return userDao.findAll();
	}

	@Override
	public List<User> findUserByname( String name) {
		// TODO Auto-generated method stub
		 return userMapper.queryUserByname(name);
	}

}
