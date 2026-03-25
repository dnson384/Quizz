"use client";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import auth_theme from "../../../public/auth_theme.png";
import useAuth from "@/presentation/hooks/Auth/useAuth";
import { useAuthStore, useRoleStore } from "@/presentation/store/auth.store";

export default function Auth() {
  const {
    fieldData,
    error,
    acceptTerm,
    setFieldData,
    handleInputChange,
    setRole,
    handleRoleChoice,
    handleCloseAuthForm,
    handleSubmitLoginForm,
    handleSubmitRegisterForm,
    handleAcceptTermChange,
  } = useAuth();

  // Check phương thức
  const method = useAuthStore((state) => state.authMethod);
  const [isLogin, setIsLogin] = useState(method === "login");

  // Check role
  const role = useRoleStore((state) => state.authRole);
  useEffect(() => {
    setIsLogin(method === "login");
    if (role) {
      setRole(role);
    }
  }, [method, role]);

  const [showPassword, setShowPassword] = useState(false);
  const [inputType, setInputType] = useState("password");

  const handleTitleClick = (event: React.MouseEvent<HTMLHeadElement>) => {
    setShowPassword(false);
    setInputType("password");
    setFieldData({});

    const target = event.target as HTMLElement;
    if (target.id === "register_title") {
      setIsLogin(false);
      document.getElementById("login_title")?.classList.add("text-gray-500");
      target.classList.remove("text-gray-500");
    } else {
      setIsLogin(true);
      document.getElementById("register_title")?.classList.add("text-gray-500");
      target.classList.remove("text-gray-500");
    }
  };

  const handleShowPassword = () => {
    if (showPassword === false) {
      setShowPassword(!showPassword);
      setInputType("text");
    } else {
      setShowPassword(!showPassword);
      setInputType("password");
    }
  };

  return (
    <>
      <div className="flex">
        {/* Image theme */}
        <div className="relative h-screen w-[50%] select-none hidden xl:block">
          <Image
            src={auth_theme}
            alt="auth_theme"
            className="absolute h-screen object-cover "
          />
          <h1 className="absolute m-20 text-[2.5rem] font-bold">
            Cách tốt nhất để học. <br />
            Đăng ký miễn phí.
          </h1>
        </div>

        {/* Đăng ký, đăng nhập */}
        <div className="sm:p-4 mx-auto xl:w-[50%] w-screen relative">
          {/* Thông báo lỗi */}
          {error && (
            <div className="absolute top-2 inset-x-0 flex justify-center">
              <div className="flex items-center gap-2 bg-red-100 w-fit h-fit p-2 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 512 512"
                >
                  <path
                    fill="#f67c6f"
                    fillRule="evenodd"
                    d="M256 42.667c117.803 0 213.334 95.53 213.334 213.333S373.803 469.334 256 469.334S42.667 373.803 42.667 256S138.197 42.667 256 42.667m48.918 134.25L256 225.836l-48.917-48.917l-30.165 30.165L225.835 256l-48.917 48.918l30.165 30.165L256 286.166l48.918 48.917l30.165-30.165L286.166 256l48.917-48.917z"
                  />
                </svg>
                <p className=" text-red-400 select-none">{error}</p>
              </div>
            </div>
          )}

          {/* Close btn */}
          <div
            id="close_auth_form_btn"
            className="flex justify-end"
            onClick={handleCloseAuthForm}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              className="cursor-pointer"
            >
              <path
                fill="currentColor"
                d="M18.3 5.71a.996.996 0 0 0-1.41 0L12 10.59L7.11 5.7A.996.996 0 1 0 5.7 7.11L10.59 12L5.7 16.89a.996.996 0 1 0 1.41 1.41L12 13.41l4.89 4.89a.996.996 0 1 0 1.41-1.41L13.41 12l4.89-4.89c.38-.38.38-1.02 0-1.4"
              />
            </svg>
          </div>

          {/* Form */}
          <div className="mx-auto mt-8 flex flex-col items-center gap-6 md:w-xl sm:w-lg w-screen sm:p-0">
            {/* Title */}
            <div className="flex gap-8 sm:justify-start justify-center w-full">
              <h1
                id="register_title"
                className={`text-[1.75rem] font-bold cursor-pointer select-none ${
                  isLogin ? "text-gray-500" : ""
                }`}
                onClick={handleTitleClick}
              >
                Đăng ký
              </h1>
              <h1
                id="login_title"
                className={`text-[1.75rem] font-bold cursor-pointer select-none ${
                  isLogin ? "" : "text-gray-500"
                }`}
                onClick={handleTitleClick}
              >
                Đăng nhập
              </h1>
            </div>

            {/* Form */}
            {isLogin ? (
              // Login Form
              <div>
                <form
                  action="submit"
                  className="flex flex-col gap-3 w-fit"
                  onSubmit={handleSubmitLoginForm}
                >
                  <div className="flex flex-col gap-1">
                    <h2 className="font-semibold text-gray-700">Email</h2>
                    <input
                      type="email"
                      name="email"
                      value={fieldData?.email || ""}
                      placeholder="Nhập địa chỉ email của bạn"
                      className="md:w-xl sm:w-lg w-screen py-2 px-3 bg-indigo-50 rounded-md placeholder:font-semibold focus:outline-indigo-500"
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="flex flex-col gap-1 w-fit">
                    <div className="flex justify-between">
                      <h2 className="font-semibold text-gray-700">Mật khẩu</h2>
                      <h2 className="font-semibold text-indigo-500 text-sm select-none cursor-pointer hover:text-indigo-700">
                        Quên mật khẩu
                      </h2>
                    </div>
                    <div className="relative flex items-center">
                      <input
                        type={inputType}
                        name="plainPassword"
                        value={fieldData?.plainPassword || ""}
                        placeholder="Nhập mật khẩu của bạn"
                        className="md:w-xl sm:w-lg w-screen py-2 px-3 bg-indigo-50 rounded-md placeholder:font-semibold focus:outline-indigo-500"
                        onChange={handleInputChange}
                      />
                      {showPassword ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          viewBox="0 0 32 32"
                          className="absolute right-3 cursor-pointer select-none"
                          onClick={handleShowPassword}
                        >
                          <path
                            fill="currentColor"
                            d="m20.525 21.94l7.768 7.767a1 1 0 0 0 1.414-1.414l-26-26a1 1 0 1 0-1.414 1.414l5.19 5.19c-3.99 3.15-5.424 7.75-5.444 7.823c-.16.53.14 1.08.67 1.24s1.09-.14 1.25-.67c.073-.254 1.358-4.323 4.926-6.99l3.175 3.175a6 6 0 1 0 8.465 8.465m-1.419-1.42a4 4 0 1 1-5.627-5.627zm-3.553-8.504l2.633 2.634c.464.303.86.7 1.164 1.163l2.634 2.634q.015-.222.016-.447a6 6 0 0 0-6.447-5.984M10.59 7.053L12.135 8.6a12.2 12.2 0 0 1 3.861-.6c9.105 0 11.915 8.903 12.038 9.29c.13.43.53.71.96.71v-.01a.993.993 0 0 0 .96-1.28C29.923 16.61 26.613 6 15.995 6c-2.07 0-3.862.403-5.406 1.053"
                          />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          viewBox="0 0 32 32"
                          className="absolute right-3 cursor-pointer select-none"
                          onClick={handleShowPassword}
                        >
                          <path
                            fill="currentColor"
                            d="M28.034 17.29c.13.43.53.71.96.71v-.01a.993.993 0 0 0 .96-1.28C29.923 16.61 26.613 6 15.995 6S2.07 16.61 2.04 16.72c-.16.53.14 1.08.67 1.24s1.09-.14 1.25-.67C4.069 16.91 6.889 8 15.996 8c9.105 0 11.915 8.903 12.038 9.29M12 18a4 4 0 1 1 8 0a4 4 0 0 1-8 0m4-6a6 6 0 1 0 0 12a6 6 0 0 0 0-12"
                          />
                        </svg>
                      )}
                    </div>
                  </div>
                  <p className="text-sm text-center md:w-xl sm:w-lg w-screen">
                    Bằng cách nhấp Đăng nhập, bạn chấp nhận{" "}
                    <strong>Điều khoản dịch vụ</strong> Và{" "}
                    <strong>Chính sách quyền riêng tư</strong> của Quizlet
                  </p>
                  <button
                    type="submit"
                    className="bg-indigo-500 text-white py-4 rounded-full font-bold select-none cursor-pointer md:w-xl sm:w-lg w-screen"
                  >
                    Đăng Nhập
                  </button>
                </form>
              </div>
            ) : (
              // Register Form
              <div>
                <form
                  action="submit"
                  className="flex flex-col gap-3 w-fit"
                  onSubmit={handleSubmitRegisterForm}
                >
                  {/* Email */}
                  <div className="flex flex-col gap-1">
                    <h2 className="font-semibold text-gray-700">Email</h2>
                    <input
                      type="email"
                      name="email"
                      value={fieldData?.email || ""}
                      placeholder="Nhập địa chỉ email của bạn"
                      className="md:w-xl sm:w-lg w-screen py-2 px-3 bg-indigo-50 rounded-md placeholder:font-semibold focus:outline-indigo-500"
                      onChange={handleInputChange}
                    />
                  </div>
                  {/* Username */}
                  <div className="flex flex-col gap-1">
                    <h2 className="font-semibold text-gray-700">
                      Tên người dùng
                    </h2>
                    <input
                      type="text"
                      name="username"
                      value={fieldData?.username || ""}
                      placeholder="Nhập tên người dùng của bạn"
                      className="md:w-xl sm:w-lg w-screen py-2 px-3 bg-indigo-50 rounded-md placeholder:font-semibold focus:outline-indigo-500"
                      onChange={handleInputChange}
                    />
                  </div>
                  {/* Password */}
                  <div className="flex flex-col gap-1 w-fit">
                    <h2 className="font-semibold text-gray-700">Mật khẩu</h2>
                    <div className="relative flex items-center">
                      <input
                        type={inputType}
                        name="plainPassword"
                        value={fieldData?.plainPassword || ""}
                        placeholder="Nhập mật khẩu của bạn"
                        className="md:w-xl sm:w-lg w-screen py-2 px-3 bg-indigo-50 rounded-md placeholder:font-semibold focus:outline-indigo-500"
                        onChange={handleInputChange}
                      />
                      {showPassword ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          viewBox="0 0 32 32"
                          className="absolute right-3 cursor-pointer select-none"
                          onClick={handleShowPassword}
                        >
                          <path
                            fill="currentColor"
                            d="m20.525 21.94l7.768 7.767a1 1 0 0 0 1.414-1.414l-26-26a1 1 0 1 0-1.414 1.414l5.19 5.19c-3.99 3.15-5.424 7.75-5.444 7.823c-.16.53.14 1.08.67 1.24s1.09-.14 1.25-.67c.073-.254 1.358-4.323 4.926-6.99l3.175 3.175a6 6 0 1 0 8.465 8.465m-1.419-1.42a4 4 0 1 1-5.627-5.627zm-3.553-8.504l2.633 2.634c.464.303.86.7 1.164 1.163l2.634 2.634q.015-.222.016-.447a6 6 0 0 0-6.447-5.984M10.59 7.053L12.135 8.6a12.2 12.2 0 0 1 3.861-.6c9.105 0 11.915 8.903 12.038 9.29c.13.43.53.71.96.71v-.01a.993.993 0 0 0 .96-1.28C29.923 16.61 26.613 6 15.995 6c-2.07 0-3.862.403-5.406 1.053"
                          />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          viewBox="0 0 32 32"
                          className="absolute right-3 cursor-pointer select-none"
                          onClick={handleShowPassword}
                        >
                          <path
                            fill="currentColor"
                            d="M28.034 17.29c.13.43.53.71.96.71v-.01a.993.993 0 0 0 .96-1.28C29.923 16.61 26.613 6 15.995 6S2.07 16.61 2.04 16.72c-.16.53.14 1.08.67 1.24s1.09-.14 1.25-.67C4.069 16.91 6.889 8 15.996 8c9.105 0 11.915 8.903 12.038 9.29M12 18a4 4 0 1 1 8 0a4 4 0 0 1-8 0m4-6a6 6 0 1 0 0 12a6 6 0 0 0 0-12"
                          />
                        </svg>
                      )}
                    </div>
                  </div>
                  {/* Confirm Password */}
                  <div className="flex flex-col gap-1 w-fit">
                    <h2 className="font-semibold text-gray-700">
                      Xác nhận mật khẩu
                    </h2>
                    <div className="relative flex items-center">
                      <input
                        type={inputType}
                        name="confirmPassword"
                        value={fieldData?.confirmPassword || ""}
                        placeholder="Xác nhận mật khẩu của bạn"
                        className="md:w-xl sm:w-lg w-screen py-2 px-3 bg-indigo-50 rounded-md placeholder:font-semibold focus:outline-indigo-500"
                        onChange={handleInputChange}
                      />
                    </div>
                  </div>
                  {/* Role */}
                  <div className="w-full flex flex-col gap-1">
                    <h2 className="font-semibold text-gray-700">Bạn là:</h2>
                    <div className="grid grid-cols-2 gap-3">
                      <div
                        id="student"
                        className={`text-center p-2 rounded-full select-none cursor-pointer ${
                          fieldData?.role === "STUDENT"
                            ? "bg-indigo-500 text-white"
                            : "bg-indigo-50 text-black hover:bg-indigo-100 "
                        }`}
                        onClick={handleRoleChoice}
                      >
                        Học sinh
                      </div>
                      <div
                        id="teacher"
                        className={`text-center p-2 rounded-full select-none cursor-pointer ${
                          fieldData?.role === "TEACHER"
                            ? "bg-indigo-500 text-white"
                            : "bg-indigo-50 text-black hover:bg-indigo-100"
                        }`}
                        onClick={handleRoleChoice}
                      >
                        Giáo viên
                      </div>
                    </div>
                  </div>
                  {/* Accept Terms */}
                  <div className="flex gap-2 items-center">
                    <input
                      type="checkbox"
                      name="terms_checkbox"
                      id="term_checkbox"
                      checked={acceptTerm}
                      onChange={handleAcceptTermChange}
                    />
                    <label htmlFor="term_checkbox" className="select-none">
                      Tôi chấp nhận Điều khoản dịch vụ Và Chính sách quyền riêng
                      tư
                    </label>
                  </div>

                  <button
                    type="submit"
                    className="bg-indigo-500 text-white py-4 rounded-full font-bold select-none cursor-pointer md:w-xl sm:w-lg w-screen"
                  >
                    Đăng ký
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
