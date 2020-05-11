package com.user.service;

import java.util.List;

import com.user.domain.User;


/**
 * @author Administrator
 *
 */
public interface UserService {
	
	/**
	 * @return
	 */
	public List<User> findAllUser();
	
	/**
	 * 根据名字查询用户
	 * @return
	 */
	public List<User> findUserByname(String name);

}
