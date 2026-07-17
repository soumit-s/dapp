import z from "zod";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useApiClient } from "~/hooks/use-api-client";
import axios from "axios";
import { StatusCodes } from "http-status-codes";
import { useNavigate } from "react-router";
import { Button } from "~/components/ui/button";
import { Field, FieldError, FieldLabel } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { useAuthToken } from "~/hooks/use-auth-token";

const loginFormSchema = z.object({
  email: z.email(),
  password: z.string().min(4),
});

type LoginFormSchema = z.infer<typeof loginFormSchema>;

export default function LoginPage() {
  const {
    control,
    handleSubmit,
    setError,
  } = useForm<LoginFormSchema>({
    resolver: zodResolver(loginFormSchema),
    defaultValues: { email: "", password: "" },
  });
  const { setToken } = useAuthToken();
  const apiClient = useApiClient();
  const navigate = useNavigate();
  const login = async (data: LoginFormSchema) => {
    try {
      const token = await apiClient
        .post<string>("/api/v1/admin/auth/login/basic", { ...data })
        .then((res) => res.data);
      // Store the token
      setToken(token);
      // Redirect to the dashboard page.
      navigate("/dashboard");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          if (error.status == StatusCodes.UNAUTHORIZED) {
            setError("password", { message: "Invalid credentials" });
          } else if (error.status == StatusCodes.INTERNAL_SERVER_ERROR) {
            setError("root", { message: "Something went wrong :(" });
          }
          return;
        }
      }
      console.error(error)
      throw error;
    }
  };

  return (
    <div className="pt-40 flex justify-center">
      <form onSubmit={handleSubmit(login)} className="flex flex-col gap-4 w-80">
        <Controller
          control={control}
          name="email"
          render={({ fieldState, field }) => (
            <Field data-invalid={fieldState.invalid}>
              <FieldLabel htmlFor="form-login-email">Email</FieldLabel>
              <Input
                {...field}
                id="form-login-email"
                autoComplete="off"
                placeholder="xyz@example.com"
                aria-invalid={fieldState.invalid}
              />
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />

        <Controller
          control={control}
          name="password"
          render={({ fieldState, field }) => (
            <Field data-invalid={fieldState.invalid}>
              <FieldLabel htmlFor="form-login-password">Password</FieldLabel>
              <Input
                {...field}
                type="password"
                id="form-login-password"
                autoComplete="off"
                placeholder="Enter Password"
                aria-invalid={fieldState.invalid}
              />
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />
        <Button type="submit">Login</Button>
      </form>
    </div>
  );
}
