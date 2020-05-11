package com.user.test;

import java.util.List;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.env.Environment;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.user.Application;
import com.user.domain.User;
import com.user.service.UserService;


@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(classes=Application.class)
public class JunitTest {

	@Autowired
	private UserService userService;
	
	@Autowired
	private Environment env;
	
	
	@Test
	public void test() {
	List<User>	user = userService.findAllUser();
	System.out.println(user.get(0));
	}
	
	@Test
	public void testEnv() {
	 
	System.out.println(env.getProperty("spring.jpa.database")+"-------------");
	}
}
