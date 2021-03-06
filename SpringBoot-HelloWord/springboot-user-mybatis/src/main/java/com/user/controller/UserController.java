package com.user.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.user.domain.User;
import com.user.service.UserService;

/**
 * @author Administrator 用户控制
 */
@RestController
@RequestMapping("/user")
public class UserController {

	@Autowired
	private UserService userService;

	@RequestMapping("/findUsserByname/{name}")
	public List<User> findUserByname(@PathVariable("name") String name) {

		return userService.findUserByname(name);

	}
	
	@RequestMapping("/findAllUsser")
	public List<User> findAllUser() {
		return userService.findAllUser();

	}
}
