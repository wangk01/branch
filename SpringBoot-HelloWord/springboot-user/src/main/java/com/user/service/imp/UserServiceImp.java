package com.user.service.imp;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.user.dao.UserDao;
import com.user.domain.User;
import com.user.service.UserService;

@Service("userService")
public class UserServiceImp implements UserService {

	@Autowired
	private UserDao userDao;
	
	@Override
	public List<User> findAllUser() {
		// TODO Auto-generated method stub
		return userDao.findAll();
	}

}
