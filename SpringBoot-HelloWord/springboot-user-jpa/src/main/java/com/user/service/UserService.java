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

}
