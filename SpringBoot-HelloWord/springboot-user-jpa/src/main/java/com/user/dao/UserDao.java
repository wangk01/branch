package com.user.dao;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.user.domain.User;

/**
 * 持久层
 * @author Administrator
 *
 */
@Repository("userDao")
public interface UserDao  extends JpaRepository<User, Long>{

}
